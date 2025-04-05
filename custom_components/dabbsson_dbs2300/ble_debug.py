import asyncio
import sys
import json
import struct
import base64
import paho.mqtt.client as mqtt
from bleak import BleakScanner
from datetime import datetime
from Crypto.Cipher import AES

DEFAULT_ADDRESS = "1C:90:FF:4A:84:E0"
ADDRESS = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ADDRESS
LOGFILE = "ble_monitor.log"

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_USER = "mqttadmin"
MQTT_PASS = "Hfsc7110t"
MQTT_TOPIC_BASE = "dabbsson/dbs2300"
MQTT_DISCOVERY_PREFIX = "homeassistant"

LOCAL_KEY = b"yn^gA(Y;aN_@W)}T"

def discovery_topic(sensor_id):
    return f"{MQTT_DISCOVERY_PREFIX}/sensor/dbs2300_{sensor_id}/config"

def discovery_payload(name, topic, unit):
    return json.dumps({
        "name": name,
        "state_topic": topic,
        "unique_id": f"dbs2300_{name.lower().replace(' ', '_')}",
        "unit_of_measurement": unit,
        "device": {
            "identifiers": ["dbs2300"],
            "manufacturer": "Dabbsson",
            "model": "DBS2300H",
            "name": "Dabbsson DBS2300"
        }
    })

mqttc = mqtt.Client()
mqttc.username_pw_set(MQTT_USER, MQTT_PASS)
mqttc.connect(MQTT_HOST, MQTT_PORT, 60)

def mqtt_publish(topic, value):
    mqttc.publish(topic, value, retain=True)

def mqtt_discovery():
    sensors = {
        "soc_dbs2300": ("DBS2300 SoC", "%"),
        "temp_dbs2300": ("DBS2300 Temperatur", "°C"),
        "dc_input": ("DBS2300 DC Input", "W"),
        "dc_output": ("DBS2300 DC Output", "W"),
        "output_power": ("DBS2300 AC Output", "W"),
        "ac_output_onoff": ("DBS2300 AC Output (ON/OFF)", None),
        "usb_5v_onoff": ("DBS2300 USB 5V", None),
        "dc_12v_onoff": ("DBS2300 DC 12V", None),
        "ac_input_power": ("DBS2300 AC Input", "W"),
        "val_205": ("DBS3000B Wert 205", "W"),
        "val_206": ("DBS3000B Wert 206", "W"),
        "val_208": ("DBS3000B Wert 208", "W"),
        "val_209": ("DBS3000B Wert 209", "W"),
        "val_220": ("DBS3000B Wert 220", "W"),
        "val_221": ("DBS3000B Wert 221", "W"),
        "val_222": ("DBS3000B Wert 222", "W"),
    }
    for key, (name, unit) in sensors.items():
        topic = f"{MQTT_TOPIC_BASE}/tuya/{key}"
        payload = discovery_payload(name, topic, unit)
        mqttc.publish(discovery_topic(key), payload, retain=True)

def log_to_file(message: str):
    try:
        with open(LOGFILE, "a") as f:
            f.write(f"{datetime.now()} {message}\n")
    except Exception as e:
        print(f"Fehler beim Schreiben ins Logfile: {e}")

DPID_MAP = {
    1: "soc_dbs2300",
    10: "temp_dbs2300",
    103: "dc_input",
    105: "dc_output",
    108: "output_power",
    109: "ac_output_onoff",
    111: "usb_5v_onoff",
    112: "dc_12v_onoff",
    123: "ac_input_power",
    138: "soc_dbs3000b",
    156: "encoded_dbs3000b",
}

def decrypt_aes(data: bytes) -> bytes:
    cipher = AES.new(LOCAL_KEY, AES.MODE_ECB)
    return cipher.decrypt(data)

def parse_encoded_dbs3000b(hexdata):
    result = {}
    try:
        encrypted = bytes.fromhex(hexdata)
        decrypted = decrypt_aes(encrypted)
        result["val_205"] = int.from_bytes(decrypted[0:4], 'big')
        result["val_206"] = int.from_bytes(decrypted[4:8], 'big')
        result["val_208"] = int.from_bytes(decrypted[8:12], 'big')
        result["val_209"] = int.from_bytes(decrypted[12:16], 'big')
        result["val_220"] = int.from_bytes(decrypted[16:20], 'big')
        result["val_221"] = int.from_bytes(decrypted[20:24], 'big')
        result["val_222"] = int.from_bytes(decrypted[24:28], 'big')
    except Exception as e:
        result["decode_error"] = str(e)
    return result

def parse_tuya_payload(payload_hex):
    try:
        payload = bytes.fromhex(payload_hex)
        results = {}
        i = 0
        while i < len(payload):
            dpid = payload[i]
            dtype = payload[i + 1]
            dlen = int.from_bytes(payload[i + 2:i + 4], "big")
            dval = payload[i + 4:i + 4 + dlen]
            key_name = DPID_MAP.get(dpid, f"unknown_{dpid}")

            if dpid == 156:
                nested = parse_encoded_dbs3000b(dval.hex())
                results.update(nested)
                for k, v in nested.items():
                    mqtt_publish(f"{MQTT_TOPIC_BASE}/tuya/{k}", v)
            else:
                if dtype == 0x02 or dtype == 0x00:
                    val = int.from_bytes(dval, "big")
                else:
                    val = dval.hex()
                results[key_name] = val
                mqtt_publish(f"{MQTT_TOPIC_BASE}/tuya/{key_name}", val)
            i += 4 + dlen
        return results
    except Exception as e:
        return {"error": str(e)}

async def monitor_advertising():
    print("\n--- BLE Advertising Monitor ---")
    while True:
        try:
            devices = await BleakScanner.discover(timeout=5.0)
            for d in devices:
                if d.address == ADDRESS:
                    print(f"{datetime.now()} Found {d.name} @ {d.address}, RSSI: {d.rssi}")
                    md = d.metadata.get("manufacturer_data", {})
                    if 0x2000 in md:
                        raw_hex = md[0x2000].hex()
                        parsed = parse_tuya_payload(raw_hex)
                        log_to_file(json.dumps(parsed))
                        print(json.dumps(parsed, indent=2))
            await asyncio.sleep(10)
        except Exception as e:
            print(f"BLE scan error: {e}")
            await asyncio.sleep(10)

# MQTT Sniffer
def on_mqtt_message(client, userdata, msg):
    payload = msg.payload.decode()
    message = f"MQTT RECEIVED ← Topic: {msg.topic}, Payload: {payload}"
    print(message)
    log_to_file(message)

async def mqtt_sniffer():
    mqttc.on_message = on_mqtt_message
    mqttc.subscribe("dabbsson/#")
    mqttc.loop_start()

# Main
async def main():
    mqtt_discovery()
    await asyncio.gather(
        monitor_advertising(),
        mqtt_sniffer()
    )

asyncio.run(main())
