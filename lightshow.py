#!/usr/bin/env python3

import asyncio
import random
from kasa import Discover
from time import sleep

stable_lights = ["Stove Lights", "Kitchen Lights"]


async def main():
    devices = await Discover.discover()
    while True:
        device_list = list(devices.values())
        random.shuffle(device_list)
        for dev in device_list:
            await dev.update()
            if not dev.alias in stable_lights:
                if dev.is_on: 
                    print(f"Turn {dev.alias} off")
                    await dev.turn_off()
                else: 
                    print(f"Turn {dev.alias} on")
                    await dev.turn_on()
        sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
