import logging
import voluptuous as vol

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.core import HomeAssistant
from homeassistant.components import mqtt

CONF_MQTT_TOPIC = "mqtt_topic"

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
):
    if discovery_info is None:
        return

    name = discovery_info[CONF_NAME]
    topic = discovery_info[CONF_MQTT_TOPIC]
    async_add_entities([DabbssonSensor(name, topic)])

class DabbssonSensor(SensorEntity):
    def __init__(self, name: str, topic: str):
        self._name = name
        self._topic = topic
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_added_to_hass(self):
        await mqtt.async_subscribe(self.hass, self._topic, self.message_received, 1)

    @callback
    def message_received(self, msg):
        _LOGGER.debug(f"MQTT message for {self._name}: {msg.payload}")
        self._state = msg.payload
        self.async_write_ha_state()
