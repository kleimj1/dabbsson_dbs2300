
Oder nutze den direkten Button:

[![In Home Assistant hinzufügen](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/kleimj1/dabbsson_dbs2300)

---

## ⚙️ Konfiguration (UI)

| Feld                 | Beschreibung                                   |
|----------------------|-----------------------------------------------|
| `device_id`          | Die Tuya-Geräte-ID deines DBS2300             |
| `local_key`          | Der lokale Schlüssel deines DBS2300           |
| `ip`                 | Lokale IP-Adresse des DBS2300                 |
| `mqtt_host`          | MQTT Broker Hostname (z. B. `core-mosquitto`) |
| `mqtt_port`          | MQTT Port (meist `1883`)                      |
| `mqtt_topic`         | Basis-MQTT-Topic für Statusdaten              |
| `mqtt_command_topic` | Topic für eingehende Steuerbefehle            |
| `mqtt_discovery_prefix` | Meist `homeassistant`                      |

---

## 🔎 Woher bekomme ich `device_id` und `local_key`?

1. Erstelle ein Entwicklerkonto auf [https://iot.tuya.com](https://iot.tuya.com)
2. Verknüpfe dein Smart Life Konto mit Tuya
3. Navigiere zu Cloud → Devices → Dein Gerät
4. Dort findest du `Device ID` und `Local Key`

➡️ Es gibt auch Tools wie [`tuya-cli`](https://github.com/TuyaAPI/cli) oder die [Smart Life Link Tuya v2-Anleitung](https://github.com/rospogrigio/localtuya#obtain-device-id-and-local-key)

---

## 🧪 Beispiel-MQTT Topics

| Topic                        | Inhalt                     |
|------------------------------|----------------------------|
| `dabbsson/status/1`         | SoC Batterie 1 in %        |
| `dabbsson/status/10`        | Temperatur in °C           |
| `dabbsson/status/109`       | AC Out an/aus (Schalter)   |
| `dabbsson/command/109`      | Steuerung `true`/`false`   |

---

## 📚 Weitere Informationen

- 📘 [tinytuya GitHub Projekt](https://github.com/jasonacox/tinytuya)
- 🧰 [paho-mqtt Python Client](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)

---

## 🙌 Credits

- Add-on entwickelt für den **Dabbsson DBS2300**  
- MQTT-Anbindung inspiriert durch @nilsTI  
- MQTT Auto-Discovery nach [Home Assistant Schema](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery)

---

## 📥 Feedback, Issues, Erweiterung?

Erstelle ein GitHub Issue oder Forke das Projekt!  
Ich freue mich über Community-Beiträge 😊

---

## 🧪 Beispiel:

```yaml
# In MQTT: Automatisch generierte Entitäten
sensor.dabbsson_soc_batterie_1
switch.dabbsson_ac_out_an
sensor.dabbsson_temperatur
sensor.dabbsson_netzspannung
