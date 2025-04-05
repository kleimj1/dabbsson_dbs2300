# custom_components/dabbsson_dbs2300/sensor.py

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, BLE_KEYS

async def async_setup_entry(hass, config_entry: ConfigEntry, async_add_entities):
    client = hass.data[DOMAIN][config_entry.entry_id]["client"]
    sensors = [
        DBSensor(client, "State of Charge", BLE_KEYS["soc"], "%"),
        DBSensor(client, "Temperature", BLE_KEYS["temperature"], "°C"),
        DBSensor(client, "DC Input", BLE_KEYS["dc_input"], "W"),
        DBSensor(client, "DC Output", BLE_KEYS["dc_output"], "W"),
        DBSensor(client, "Power Output", BLE_KEYS["power_output"], "W"),
        DBSensor(client, "AC Input Power", BLE_KEYS["ac_input_power"], "W"),
        DBSensor(client, "DBS3000B SoC", BLE_KEYS["soc_dbs3000b"], "%"),
        DBSensor(client, "Encoded Info DBS3000B", BLE_KEYS["encoded_info"], None),
    ]
    async_add_entities(sensors, True)

class DBSensor(SensorEntity):
    def __init__(self, client, name, key, unit):
        self._client = client
        self._key = key
        self._attr_name = f"DBS2300 {name}"
        self._attr_unit_of_measurement = unit
        self._attr_state = None

    async def async_update(self):
        data = await self._client.read_gatt_char(self._key)
        self._attr_state = int.from_bytes(data[:2], byteorder='little')
