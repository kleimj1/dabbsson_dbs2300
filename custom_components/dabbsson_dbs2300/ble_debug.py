import asyncio
import sys
from bleak import BleakClient
from datetime import datetime

DEFAULT_ADDRESS = "1C:90:FF:4A:84:E0"
ADDRESS = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ADDRESS

UUIDS_TO_MONITOR = {
    "status_notify":   "00002b10-0000-1000-8000-00805f9b34fb",
    "feature_control": "00002b29-0000-1000-8000-00805f9b34fb",
    "read_value_1":    "00002b2a-0000-1000-8000-00805f9b34fb",
}

LOGFILE = "ble_monitor.log"

def log_to_file(message: str):
    with open(LOGFILE, "a") as f:
        f.write(message + "\n")

async def run():
    async with BleakClient(ADDRESS) as client:
        print(f"# Connected to {ADDRESS}")
        log_to_file(f"# Connected to {ADDRESS} at {datetime.now()}")
        
        print("\\n=== GATT Service Dump ===")
        log_to_file("\\n=== GATT Service Dump ===")
        services = await client.get_services()
        for service in services:
            log_to_file(f"Service: {service.uuid}")
            for char in service.characteristics:
                props = ', '.join(char.properties)
                line = f"Char: uuid={char.uuid}, handle={hex(char.handle)}, props=[{props}]"
                print(line)
                log_to_file(line)

        print("\\n=== Begin Live Monitoring ===")
        log_to_file("\\n=== Begin Live Monitoring ===")

        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\\n--- {timestamp} ---")
            log_to_file(f"\\n--- {timestamp} ---")

            for name, uuid in UUIDS_TO_MONITOR.items():
                try:
                    data = await client.read_gatt_char(uuid)
                    hex_value = data.hex()
                    int_value = int.from_bytes(data, byteorder='little')
                    line = f"{name} [{uuid}]: raw={hex_value}, int={int_value}"
                except Exception as e:
                    line = f"{name} [{uuid}]: ERROR -> {e}"

                print(line)
                log_to_file(line)

            await asyncio.sleep(5)

asyncio.run(run())
