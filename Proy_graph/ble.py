# # Lib para HeartRateService class
# from bluez_peripheral.gatt.service import Service
# from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags

# import struct
# # Lib para Main
# from bluez_peripheral.util import *
# from bluez_peripheral.advert import Advertisement
# from bluez_peripheral.agent import NoIoAgent
# import asyncio

# class HeartRateService(Service):
    # def __init__(self):
        # # Base 16 service UUID, This should be a primary service.
        # super().__init__("180D", True)

    # @characteristic("2A37", CharFlags.NOTIFY)
    # def heart_rate_measurement(self, options):
        # # This function is called when the characteristic is read.
        # # Since this characteristic is notify only this function is a placeholder.
        # # You don't need this function Python 3.9+ (See PEP 614).
        # # You can generally ignore the options argument 
        # # (see Advanced Characteristics and Descriptors Documentation).
        # pass

    # def update_heart_rate(self, new_rate):
        # # Call this when you get a new heartrate reading.
        # # Note that notification is asynchronous (you must await something at some point after calling this).
        # flags = 0

        # # Bluetooth data is little endian.
        # rate = struct.pack("<BB", flags, new_rate)
        # self.heart_rate_measurement.changed(rate)
        


# async def main():
    # # Alternativly you can request this bus directly from dbus_next.
    # bus = await get_message_bus()

    # service = HeartRateService()
    # await service.register(bus)

    # # An agent is required to handle pairing 
    # agent = NoIoAgent()
    # # This script needs superuser for this to work.
    # await agent.register(bus)

    # adapter = await Adapter.get_first(bus)

    # # Start an advert that will last for 60 seconds.
    # advert = Advertisement("Heart Monitor", ["180D"], 0x0340, 60)
    # await advert.register(bus, adapter)

    # while True:
        # # Update the heart rate.
        # service.update_heart_rate(120)
        # # Handle dbus requests.
        # await asyncio.sleep(5)

    # await bus.wait_for_disconnect()

# if __name__ == "__main__":
    # asyncio.run(main())

"""Copyright 2021-2022 Google LLC
#
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
#
     https://www.apache.org/licenses/LICENSE-2.0
#
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import asyncio
import sys
import os
import logging
from bumble.colors import color

from bumble.device import Device
from bumble.transport import open_transport_or_link


# -----------------------------------------------------------------------------
async def main():
    if len(sys.argv) < 2:
        print('Usage: run_scanner.py <transport-spec> [filter]')
        print('example: run_scanner.py usb:0')
        return

    print('<<< connecting to HCI...')
    async with await open_transport_or_link(sys.argv[1]) as (hci_source, hci_sink):
        print('<<< connected')
        filter_duplicates = len(sys.argv) == 3 and sys.argv[2] == 'filter'

        device = Device.with_hci('raspberrypi', 'DC:A6:32:68:FA:17', hci_source, hci_sink)

        @device.on('advertisement')
        def _(advertisement):
            address_type_string = ('PUBLIC', 'RANDOM', 'PUBLIC_ID', 'RANDOM_ID')[
                advertisement.address.address_type
            ]
            address_color = 'yellow' if advertisement.is_connectable else 'red'
            address_qualifier = ''
            if address_type_string.startswith('P'):
                type_color = 'cyan'
            else:
                if advertisement.address.is_static:
                    type_color = 'green'
                    address_qualifier = '(static)'
                elif advertisement.address.is_resolvable:
                    type_color = 'magenta'
                    address_qualifier = '(resolvable)'
                else:
                    type_color = 'white'

            separator = '\n  '
            print(
                f'>>> {color(advertisement.address, address_color)} '
                f'[{color(address_type_string, type_color)}]'
                f'{address_qualifier}:{separator}RSSI:{advertisement.rssi}'
                f'{separator}'
                f'{advertisement.data.to_string(separator)}'
            )

        await device.power_on()
        await device.start_scanning(filter_duplicates=filter_duplicates)

        await hci_source.wait_for_termination()


# -----------------------------------------------------------------------------
logging.basicConfig(level=os.environ.get('BUMBLE_LOGLEVEL', 'DEBUG').upper())
asyncio.run(main())"""


# Copyright 2021-2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
# ~ import logging
# ~ import asyncio
# ~ import sys
# ~ import os

# ~ from bumble.gatt import (
    # ~ GATT_CHARACTERISTIC_USER_DESCRIPTION_DESCRIPTOR,
    # ~ GATT_DEVICE_INFORMATION_SERVICE,
    # ~ GATT_MANUFACTURER_NAME_STRING_CHARACTERISTIC,
    # ~ Characteristic,
    # ~ Descriptor,
    # ~ Service,
# ~ )
# ~ from bumble.device import Device
# ~ from bumble.host import Host
# ~ from bumble.controller import Controller
# ~ from bumble.link import LocalLink
# ~ from bumble.transport import open_transport_or_link


# ~ # -----------------------------------------------------------------------------
# ~ async def main():
    # ~ if len(sys.argv) != 4:
        # ~ print(
            # ~ 'Usage: run_controller.py <controller-address> <device-config> '
            # ~ '<transport-spec>'
        # ~ )
        # ~ print(
            # ~ 'example: run_controller.py F2:F3:F4:F5:F6:F7 device1.json '
            # ~ 'udp:0.0.0.0:22333,172.16.104.161:22333'
        # ~ )
        # ~ return

    # ~ print('>>> connecting to HCI...')
    # ~ async with await open_transport_or_link(sys.argv[3]) as (hci_source, hci_sink):
        # ~ print('>>> connected')

        # ~ # Create a local link
        # ~ link = LocalLink()

        # ~ # Create a first controller using the packet source/sink as its host interface
        # ~ controller1 = Controller(
            # ~ 'C1', host_source=hci_source, host_sink=hci_sink, link=link
        # ~ )
        # ~ controller1.random_address = sys.argv[1]

        # ~ # Create a second controller using the same link
        # ~ controller2 = Controller('C2', link=link)

        # ~ # Create a host for the second controller
        # ~ host = Host()
        # ~ host.controller = controller2

        # ~ # Create a device to manage the host
        # ~ device = Device.from_config_file(sys.argv[2])
        # ~ device.host = host

        # ~ # Add some basic services to the device's GATT server
        # ~ descriptor = Descriptor(
            # ~ GATT_CHARACTERISTIC_USER_DESCRIPTION_DESCRIPTOR,
            # ~ Descriptor.READABLE,
            # ~ 'My Description',
        # ~ )
        # ~ manufacturer_name_characteristic = Characteristic(
            # ~ GATT_MANUFACTURER_NAME_STRING_CHARACTERISTIC,
            # ~ Characteristic.Properties.READ,
            # ~ Characteristic.READABLE,
            # ~ "Fitbit",
            # ~ [descriptor],
        # ~ )
        # ~ device_info_service = Service(
            # ~ GATT_DEVICE_INFORMATION_SERVICE, [manufacturer_name_characteristic]
        # ~ )
        # ~ device.add_service(device_info_service)

        # ~ # Debug print
        # ~ for attribute in device.gatt_server.attributes:
            # ~ print(attribute)

        # ~ await device.power_on()
        # ~ await device.start_advertising()
        # ~ await device.start_scanning()

        # ~ await hci_source.wait_for_termination()


# ~ # -----------------------------------------------------------------------------
# ~ logging.basicconfig(level=os.environ.get('bumble_loglevel', 'debug').upper())
# ~ asyncio.run(main())

# ~ from bluetooth.ble import DiscoveryService

# ~ service = DiscoveryService("hci0")
# ~ devices = service.discover(10)

# ~ for address, name in devices.items():
	# ~ print("Name : {}, address: {}".format(name, address))

#(devices.items())


# ~ # -----------------------------------------------------------------------------
"""PyBluez example read_name.py

Copyright (C) 2014, Oscar Acena <oscaracena@gmail.com>
This software is under the terms of GPLv3 or later.
"""

# ~ import sys

# ~ from bluetooth.ble import GATTRequester


# ~ class Reader:

    # ~ def __init__(self, address):
        # ~ self.requester = GATTRequester(address, False)
        # ~ self.connect()
        # ~ self.request_data()

    # ~ def connect(self):
        # ~ print("Connecting...", end=" ")
        # ~ sys.stdout.flush()

        # ~ self.requester.connect(True)
        # ~ print("OK.")

    # ~ def request_data(self):
        # ~ data = self.requester.read_by_uuid(
            # ~ "411fcc1c-e7a5-4a61-82fe-0004993dd1f4")[0]
        # ~ try:
            # ~ print("Device name:", data.decode("utf-8"))
        # ~ except AttributeError:
            # ~ print("Device name:", data)


# ~ if __name__ == "__main__":
    # ~ if len(sys.argv) < 2:
        # ~ print("Usage: {} <addr>".format(sys.argv[0]))
        # ~ sys.exit(1)

    # ~ Reader(sys.argv[1])
    # ~ print("Done.")
    

#!/usr/bin/env python3

# ~ # -----------------------------------------------------------------------------
"""PyBluez simple example inquiry.py

Performs a simple device inquiry followed by a remote name request of each
discovered device

Author: Albert Huang <albert@csail.mit.edu>
$Id: inquiry.py 401 2006-05-05 19:07:48Z albert $
"""

import bluetooth

print("Performing inquiry...")

nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
                                            flush_cache=True, lookup_class=False)

print("Found {} devices".format(len(nearby_devices)))

for addr, name in nearby_devices:
    try:
        print("   {} - {}".format(addr, name))
    except UnicodeEncodeError:
        print("   {} - {}".format(addr, name.encode("utf-8", "replace")))


#!/usr/bin/env python3
"""PyBluez ble example beacon.py

Advertises a bluethooth low energy beacon for 15 seconds.
"""

import time

from bluetooth.ble import BeaconService

service = BeaconService()

service.start_advertising("11111111-2222-3333-4444-555555555555",
                          1, 1, 1, 200)
time.sleep(15)
service.stop_advertising()

print("Done.")
