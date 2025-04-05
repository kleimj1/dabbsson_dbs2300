# custom_components/dabbsson_dbs2300/ble_debug.py

import asyncio
from bleak import BleakClient

async def main():
    address = "1C:90:FF:4A:84:E0"
    async with BleakClient(address) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  Char: {char.uuid} - Properties: {char.properties}")

asyncio.run(main())
