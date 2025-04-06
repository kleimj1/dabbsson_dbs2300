import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from .const import DOMAIN, CONF_MQTT_TOPIC

class DabbssonConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
            )

        data_schema = vol.Schema({
            vol.Required(CONF_NAME): str,
            vol.Required(CONF_MQTT_TOPIC): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
