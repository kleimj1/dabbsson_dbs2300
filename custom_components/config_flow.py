from homeassistant import config_entries
import voluptuous as vol

class DabbssonFlowHandler(config_entries.ConfigFlow, domain="dabbsson_dbs2300"):
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Dabbsson DBS2300", data=user_input)

        data_schema = vol.Schema({
            vol.Required("ble_address"): str
        })
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

# Hinweis:
# parse_ble_data ist eine Hilfsfunktion, die du basierend auf der BLE-Datenstruktur implementierst.
# Die Schlüssel müssen entsprechend der BLE-GATT-Spezifikation des DBS2300 zugeordnet sein.
