# custom_components/dabbsson_dbs2300/__init__.py

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from bleak import BleakClient

from .const import DOMAIN

PLATFORMS = ["sensor", "switch"]
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Dabbsson DBS2300 from a config entry."""
    ble_address = entry.data["ble_address"]
    client = BleakClient(ble_address)

    try:
        await client.connect()
        _LOGGER.info("Connected to DBS2300 at %s", ble_address)
    except Exception as e:
        _LOGGER.error("Could not connect to DBS2300 at %s: %s", ble_address, e)
        return False

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "client": client,
        "address": ble_address,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    client = hass.data[DOMAIN][entry.entry_id]["client"]
    try:
        await client.disconnect()
    except Exception as e:
        _LOGGER.warning("Error disconnecting from DBS2300: %s", e)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
