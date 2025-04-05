import asyncio
import sys
import json
import struct
import paho.mqtt.client as mqtt
from bleak import BleakScanner, BleakClient, BleakError
from datetime import datetime

DEFAULT_ADDRESS = "1C:90:FF:4A:84:E0"
ADDRESS = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ADDRESS
LOGFILE = "ble_monitor.log"

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_USER = "mqttadmin"
MQTT_PASS = "Hfsc7110t"
MQTT_TOPIC_BASE = "dabbsson/dbs2300"
MQTT_DISCOVERY_PREFIX = "homeassistant"

def discovery_topic(sensor_id):
    return f"{MQTT_DISCOVERY_PREFIX}/sensor/dbs2300_{sensor_id}/config"

def discovery_payload(name, topic, unit):
    return json.dumps({
        "name": name,
        "state_topic": topic,
        "unique_id": name.lower().replace(" ", "_"),
        "unit_of_measurement": unit,
        "device": {
            "identifiers": ["dbs2300"],
            "manufacturer": "Dabbsson",
            "model": "DBS2300",
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
        "ac_output_onoff": ("DBS2300 AC Output", None),
        "status_notify": ("DBS2300 Notify (GATT)", None),
    }
    for key, (name, unit) in sensors.items():
        topic = f"{MQTT_TOPIC_BASE}/tuya/{key}" if key != "status_notify" else f"{MQTT_TOPIC_BASE}/gatt/{key}"
        payload = discovery_payload(name, topic, unit)
        mqttc.publish(discovery_topic(key), payload, retain=True)


def log_to_file(message: str):
    with open(LOGFILE, "a") as f:
        f.write(message + "\n")


UUIDS_TO_MONITOR = {
    "status_notify":   "00002b10-0000-1000-8000-00805f9b34fb",
    "feature_control": "00002b29-0000-1000-8000-00805f9b34fb",
    "read_value_1":    "00002b2a-0000-1000-8000-00805f9b34fb",
}

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


async def advertise_scan():
    print("\n--- Tuya Advertising Sniff ---")
    scanner = BleakScanner()
    devices = await scanner.discover(timeout=5.0)
    for d in devices:
        if d.address == ADDRESS:
            print(f"Found {d.name} @ {d.address}, RSSI: {d.rssi}")
            md = d.metadata.get("manufacturer_data", {})
            if 0x2000 in md:
                raw_hex = md[0x2000].hex()
                parsed = parse_tuya_payload(raw_hex)
                print("Parsed manufacturer_data:", json.dumps(parsed, indent=2))
                log_to_file(json.dumps(parsed))


async def connect_and_monitor():
    while True:
        try:
            async with BleakClient(ADDRESS) as client:
                print(f"\n# Connected to {ADDRESS}")
                log_to_file(f"# Connected to {ADDRESS} at {datetime.now()}")
                
                while True:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"\n--- {timestamp} ---")
                    log_to_file(f"\n--- {timestamp} ---")

                    for name, uuid in UUIDS_TO_MONITOR.items():
                        try:
                            data = await client.read_gatt_char(uuid)
                            hex_value = data.hex()
                            int_value = int.from_bytes(data, byteorder='little')
                            line = f"{name} [{uuid}]: raw={hex_value}, int={int_value}"
                            mqtt_publish(f"{MQTT_TOPIC_BASE}/gatt/{name}", int_value)
                        except Exception as e:
                            line = f"{name} [{uuid}]: ERROR -> {e}"

                        print(line)
                        log_to_file(line)
                    await asyncio.sleep(5)
        except BleakError as e:
            print(f"# Connection error: {e}, retrying in 10s")
            log_to_file(f"# Connection error: {e}, retrying in 10s")
            await asyncio.sleep(10)


async def main():
    mqtt_discovery()
    await advertise_scan()
    await connect_and_monitor()

asyncio.run(main())
