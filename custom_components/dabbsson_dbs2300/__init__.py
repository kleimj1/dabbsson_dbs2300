## Datei: __init__.py

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers.discovery import async_load_platform

from .const import DOMAIN, CONF_DEVICES, CONF_MQTT_TOPIC

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_DEVICES): [
                    {
                        vol.Required(CONF_NAME): cv.string,
                        vol.Required(CONF_MQTT_TOPIC): cv.string,
                    }
                ]
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    devices = config[DOMAIN][CONF_DEVICES]
    for device in devices:
        hass.async_create_task(
            async_load_platform(hass, "sensor", DOMAIN, device, config)
        )
    return True
