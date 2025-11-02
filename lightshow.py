#!/usr/bin/env python3.13

import asyncio
import random
import signal
import sys
from kasa import Discover

# stable_lights = ["Stove Lights", "Kitchen Lights"]
stable_lights = ["Stove Lights", "Kitchen Lights", "Maddie Room", "Bonus Room"]

# Flag to track if we should stop the show
stop_show = False


def signal_handler(signum, frame):
    global stop_show
    print("\n🎃 Halloween show interrupted! Stopping gracefully...")
    stop_show = True


async def main():
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    devices = await Discover.discover()
    print(f"Discovered {len(devices)} devices.")
    print("Devices:", devices)
    print("Starting Halloween light show! 🎃")
    print("Press Ctrl+C to stop the show gracefully...")

    try:
        while not stop_show:
            device_list = list(devices.values())
            random.shuffle(device_list)
            for dev in device_list:
                if stop_show:  # Check if we should stop mid-cycle
                    break
                await dev.update()
                if not dev.alias in stable_lights:
                    if dev.is_on:
                        print(f"Turn {dev.alias} off")
                        await dev.turn_off()
                    else:
                        print(f"Turn {dev.alias} on")
                        await dev.turn_on()

            if not stop_show:  # Only wait if we're not stopping
                # Random delay between 1-5 seconds for spooky unpredictability
                delay = random.uniform(1, 5)
                print(f"Waiting {delay:.1f} seconds...")
                await asyncio.sleep(delay)

    except KeyboardInterrupt:
        # This shouldn't happen now, but just in case
        pass

    print("👻 Halloween light show ended. Thanks for the spooks!")
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
