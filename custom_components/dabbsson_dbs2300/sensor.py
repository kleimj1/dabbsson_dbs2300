import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.core import HomeAssistant, callback
from homeassistant.components import mqtt

from .const import CONF_MQTT_TOPIC
from .dps_metadata import DPS_METADATA

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
    topic_base = discovery_info[CONF_MQTT_TOPIC]

    sensors = []
    for dps_id, meta in DPS_METADATA.items():
        sensors.append(DabbssonSensor(name, topic_base, dps_id, meta))

    async_add_entities(sensors)

class DabbssonSensor(SensorEntity):
    def __init__(self, device_name: str, topic_base: str, dps_id: str, meta: dict):
        self._device_name = device_name
        self._topic = f"{topic_base}/{dps_id}"
        self._dps_id = dps_id
        self._name = f"{device_name} - {meta['name']}"
        self._type = meta["type"]
        self._unit = _unit_for_type(self._type)
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return f"dabbsson_{self._device_name}_{self._dps_id}"

    @property
    def state(self):
        return self._state

    @property
    def device_class(self):
        return None  # könnte bei Bedarf gesetzt werden

    @property
    def unit_of_measurement(self):
        return self._unit

    async def async_added_to_hass(self):
        await mqtt.async_subscribe(self.hass, self._topic, self.message_received, 1)

    @callback
    def message_received(self, msg):
        payload = msg.payload
        _LOGGER.debug(f"MQTT message for {self._name}: {payload}")
        try:
            self._state = _cast(payload, self._type)
        except Exception as e:
            _LOGGER.warning(f"Fehler beim Konvertieren von {payload} für {self._name}: {e}")
        self.async_write_ha_state()

def _cast(value, expected_type):
    if expected_type == "int":
        return int(value)
    elif expected_type == "bool":
        return value.lower() == "true"
    elif expected_type == "str":
        return str(value)
    return value

def _unit_for_type(value_type: str):
    if value_type == "int":
        return "W"
    elif value_type == "bool":
        return None
    elif value_type == "str":
        return None
    return None
