# 🧠 Dabbsson DBS2300 Integration (Tuya via WLAN)

Diese benutzerdefinierte Integration ermöglicht die Einbindung des **Dabbsson DBS2300** direkt über das **lokale Tuya-Protokoll via WLAN**. Die Kommunikation erfolgt per `tinytuya`, ohne Cloud oder Bluetooth.

---

## ✅ Funktionen

- 🔌 Verbindung über WLAN (lokales Tuya-Protokoll)
- 🔄 Automatische Erstellung von Sensoren & Schaltern
- 🖥️ Schreibzugriff auf unterstützte DPS-Werte (z. B. AC Out)
- 🧠 MQTT (optional über Add-on nutzbar)
- 🔒 Keine Cloud notwendig
- 💬 Unterstützt Deutsch und Englisch

---

## 🚀 Installation über HACS

Diese Integration ist mit [HACS (Home Assistant Community Store)](https://hacs.xyz) kompatibel.

### Schritt-für-Schritt

1. Öffne Home Assistant → HACS → Integrationen
2. Klick auf „Benutzerdefinierte Repositories hinzufügen“
3. Repository-URL:

https://github.com/kleimj1/dabbsson_dbs2300


4. Kategorie: `Integration`
5. Danach: Integration wie gewohnt über `Einstellungen → Geräte & Dienste → Integration hinzufügen` einrichten

👉 Oder verwende direkt diesen Button:

[![In HACS hinzufügen](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=kleimj1&repository=dabbsson_dbs2300&category=integration)

---

## ⚙️ Konfiguration

Die Integration wird über den Home Assistant UI Konfigurationsdialog eingerichtet.

Du brauchst:

- 📦 `Device ID`  
- 🔑 `Local Key`  
- 🌐 Lokale IP-Adresse des Geräts (z. B. `192.168.178.30`)

### 🔍 Woher bekomme ich Device ID & Local Key?

1. Registriere dich bei [https://iot.tuya.com](https://iot.tuya.com)
2. Erstelle ein Cloud-Projekt & verknüpfe dein Smart Life Konto
3. Unter „Devices“ kannst du `device_id` und `local_key` einsehen

Alternativ: Tools wie [`tuya-cli`](https://github.com/TuyaAPI/cli)

---

## 🧪 Beispiel: Sensoren & Schalter

Nach der Einrichtung erscheinen z. B. folgende Entitäten in Home Assistant:

```yaml
sensor.dabbsson_soc_batterie_1
sensor.dabbsson_temperatur
sensor.dabbsson_ac_frequenz
switch.dabbsson_ac_out_an
switch.dabbsson_usb_5v_an
switch.dabbsson_dc_12v_an

Die Sensoren basieren auf den bekannten DPS-Werten, z. B.:

DPS	Beschreibung	Schreibbar
1	SoC Batterie [%]	❌
10	Temperatur [°C]	❌
109	AC Out AN	✅
111	USB 5V AN	✅
112	DC 12V AN	✅
123	Zielwert AC-Ladung [%]	✅
145	Netzspannung	✅
💬 Hinweise
Diese Integration funktioniert vollständig autark ohne Cloud oder Bluetooth.

Für MQTT-Unterstützung und HA Discovery via MQTT kannst du das passende Dabbsson Add-on verwenden.

🧠 Viel Spaß mit deinem Dabbsson in Home Assistant!
