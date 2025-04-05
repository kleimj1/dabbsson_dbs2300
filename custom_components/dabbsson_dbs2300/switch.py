# custom_components/dabbsson_dbs2300/switch.py

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

async def async_setup_entry(hass, config_entry: ConfigEntry, async_add_entities):
    client = hass.data[DOMAIN][config_entry.entry_id]["client"]
    switches = [
        DBSwitch(client, "AC Output", 109),
        DBSwitch(client, "5V Output", 111),
        DBSwitch(client, "12V Output", 112),
    ]
    async_add_entities(switches, True)

class DBSwitch(SwitchEntity):
    def __init__(self, client, name, key):
        self._client = client
        self._key = key
        self._attr_name = f"DBS2300 {name}"
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs):
        await self._client.write_gatt_char(self._key, b'\x01')
        self._attr_is_on = True

    async def async_turn_off(self, **kwargs):
        await self._client.write_gatt_char(self._key, b'\x00')
        self._attr_is_on = False

    async def async_update(self):
        data = await self._client.read_gatt_char(self._key)
        self._attr_is_on = bool(data[0])
