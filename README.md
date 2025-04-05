# Dabbsson DBS2300 Home Assistant Integration

![GitHub Release](https://img.shields.io/github/v/release/<your_username>/ha-dabbsson-dbs2300)
![HACS Supported](https://img.shields.io/badge/HACS-Supported-blue.svg)
![License](https://img.shields.io/github/license/<your_username>/ha-dabbsson-dbs2300)

## Overview
This integration allows seamless control and monitoring of your **Dabbsson DBS2300** device directly from Home Assistant. It provides comprehensive access to real-time data and control of your DBS2300 via Bluetooth Low Energy (BLE).

## Features
- Real-time battery state of charge (SoC)
- Temperature monitoring
- DC input and output monitoring
- AC input and output power monitoring
- Control AC, 5V, and 12V outputs
- Comprehensive monitoring of DBS3000B including encoded information

## Installation
### HACS (Recommended)
1. Open HACS, navigate to "Integrations", then click the three dots menu.
2. Select "Custom repositories", add `https://github.com/kleimj1/dabbsson_dbs2300`, and set category to `Integration`.
3. Search for `Dabbsson DBS2300` and install the integration.
4. Restart Home Assistant.

### Manual Installation
1. Download this repository as a ZIP.
2. Extract the folder `custom_components/dabbsson_dbs2300` into your `custom_components` directory.
3. Restart Home Assistant.

## Setup
1. Go to **Configuration → Integrations** and click on **Add Integration**.
2. Select **Dabbsson DBS2300**.
3. Enter your DBS2300 Bluetooth MAC address.
4. Finish the setup. Your device is now integrated and ready to use.

## Available Entities
| Entity | Type | Unit | Description |
|--------|------|------|-------------|
| DBS2300 State of Charge | Sensor | % | Battery charge level |
| DBS2300 Temperature | Sensor | °C | Device temperature |
| DBS2300 DC Input | Sensor | W | DC input power |
| DBS2300 DC Output | Sensor | W | DC output power |
| DBS2300 Power Output | Sensor | W | Total power output |
| DBS2300 AC Input Power | Sensor | W | AC input power |
| DBS3000B SoC | Sensor | % | DBS3000B battery charge |
| Encoded Info DBS3000B | Sensor | - | Base64 encoded DBS3000B details |
| DBS2300 AC Output | Switch | - | Toggle AC output |
| DBS2300 5V Output | Switch | - | Toggle 5V output |
| DBS2300 12V Output | Switch | - | Toggle 12V output |

## Support
If you encounter any issues or need support, please open an issue on GitHub.

## License
This integration is licensed under the [MIT License](LICENSE).
