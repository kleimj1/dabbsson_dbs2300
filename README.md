
Oder nutze den Direkt-Button:

[![In Home Assistant hinzufügen](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/kleimj1/dabbsson_dbs2300)

---

## ⚙️ Konfiguration (UI)

| Feld                 | Beschreibung                                   |
|----------------------|-----------------------------------------------|
| `device_id`          | Tuya Device ID (z. B. `bf7be7dd94a4664017zyd4`) |
| `local_key`          | Tuya Local Key (z. B. `yn^gA(Y;aN_@W)}T`)       |
| `ip`                 | Lokale IP-Adresse des DBS2300 (z. B. `192.168.178.30`) |
| `mqtt_host`          | MQTT Broker (z. B. `core-mosquitto`)          |
| `mqtt_port`          | Meist `1883`                                   |
| `mqtt_topic`         | Basis-Topic (z. B. `dabbsson`)                 |
| `mqtt_command_topic` | Topic für Befehle (z. B. `dabbsson/command`)   |
| `mqtt_discovery_prefix` | Meist `homeassistant`                      |

---

## 🔐 Woher bekomme ich `device_id` und `local_key`?

1. Erstelle einen Account auf [https://iot.tuya.com](https://iot.tuya.com)
2. Verknüpfe dein Smart Life Konto (App)
3. Gehe zu Cloud → Devices → dein Gerät
4. Dort findest du die Werte

➡️ Alternativ Tools wie [`tuya-cli`](https://github.com/TuyaAPI/cli) oder Anleitungen zur lokalen Tuya-Entschlüsselung verwenden.

---

## 📪 Beispiel-MQTT Topics

| Topic                            | Beschreibung              | Schreibbar |
|----------------------------------|----------------------------|------------|
| `dabbsson/status/1`             | SoC Batterie 1 [%]         | ❌         |
| `dabbsson/status/2`             | Kapazität Wh               | ❌         |
| `dabbsson/status/10`            | Temperatur [°C]            | ❌         |
| `dabbsson/status/25`            | AC verfügbar               | ✅         |
| `dabbsson/status/101`           | Systembereit               | ❌         |
| `dabbsson/status/102`           | Modus                      | ✅         |
| `dabbsson/status/103`           | DC Input                   | ❌         |
| `dabbsson/status/104`           | DC Input 2                 | ❌         |
| `dabbsson/status/105`           | DC Output                  | ❌         |
| `dabbsson/status/106`           | AC Output                  | ❌         |
| `dabbsson/status/108`           | Output-Leistung            | ❌         |
| `dabbsson/status/109`           | AC Out AN (Schalter)       | ✅         |
| `dabbsson/status/110`           | AC Frequenz                | ❌         |
| `dabbsson/status/111`           | USB 5V AN (Schalter)       | ✅         |
| `dabbsson/status/112`           | DC 12V AN (Schalter)       | ✅         |
| `dabbsson/status/113`           | Ladegrenze 1               | ❌         |
| `dabbsson/status/114`           | Ladegrenze 2               | ❌         |
| `dabbsson/status/115`           | ?                          | ❌         |
| `dabbsson/status/116`           | ?                          | ❌         |
| `dabbsson/status/117`           | ?                          | ❌         |
| `dabbsson/status/118`           | ?                          | ❌         |
| `dabbsson/status/120`           | AC Einschaltzeit           | ✅         |
| `dabbsson/status/121`           | AC Dauer                   | ✅         |
| `dabbsson/status/122`           | AC Ausschaltzeit           | ✅         |
| `dabbsson/status/123`           | AC Zielwert [%]            | ✅         |
| `dabbsson/status/124`           | Feature 1 (bool)           | ✅         |
| `dabbsson/status/125`           | Feature 2 (bool)           | ✅         |
| `dabbsson/status/126`           | Feature 3 (bool)           | ✅         |
| `dabbsson/status/127`           | Systemmodus                | ❌         |
| `dabbsson/status/128`           | Feature 4 (bool)           | ✅         |
| `dabbsson/status/130`           | HW Version                 | ❌         |
| `dabbsson/status/132`           | Firmware                   | ❌         |
| `dabbsson/status/133`           | BMS Version                | ❌         |
| `dabbsson/status/134`           | ?                          | ❌         |
| `dabbsson/status/135`           | ?                          | ❌         |
| `dabbsson/status/136`           | ?                          | ❌         |
| `dabbsson/status/137`           | BMS Status                 | ❌         |
| `dabbsson/status/138`           | SoC Zusatzbatterie [%]     | ❌         |
| `dabbsson/status/139`           | ?                          | ❌         |
| `dabbsson/status/140`           | Seriennummer               | ❌         |
| `dabbsson/status/143`           | ?                          | ❌         |
| `dabbsson/status/145`           | Netzspannung [V]           | ✅         |

> ✏️ Schreibbare Werte kannst du mit folgendem Befehl setzen:
>
> ```bash
> mosquitto_pub -h <mqtt_host> -t dabbsson/command/109 -m true
> ```

---

## 🧪 Beispiel: Home Assistant MQTT Discovery

Nach dem Start des Add-ons erscheinen automatisch Entitäten wie:

```yaml
sensor.dabbsson_soc_batterie_1
sensor.dabbsson_temperatur
sensor.dabbsson_netzspannung
switch.dabbsson_ac_out_an
