#!/usr/bin/env python3.13

import asyncio
import tinytuya
from kasa import Discover


async def discover_all_smart_devices():
    print("🔍 Scanning for all smart devices on your network...\n")

    # Discover TP-Link Kasa devices (you already have these)
    print("📱 TP-Link Kasa devices:")
    try:
        kasa_devices = await Discover.discover()
        if kasa_devices:
            for ip, device in kasa_devices.items():
                await device.update()
                print(f"  • {device.alias} ({device.model}) at {ip}")
        else:
            print("  No Kasa devices found")
    except Exception as e:
        print(f"  Error discovering Kasa devices: {e}")

    print(
        f"\nFound {len(kasa_devices) if 'kasa_devices' in locals() else 0} Kasa devices\n"
    )

    # Try to discover Tuya-based devices (might include some Hubspace devices)
    print("🔌 Tuya/Smart Life devices:")
    try:
        devices = tinytuya.deviceScan(False, 20)  # Scan for 20 seconds
        if devices:
            for device in devices:
                print(f"  • Device ID: {device.get('gwId', 'Unknown')}")
                print(f"    IP: {device.get('ip', 'Unknown')}")
                print(f"    Version: {device.get('version', 'Unknown')}")
                print(f"    Name: {device.get('name', 'Unknown')}")
                print()
        else:
            print("  No Tuya devices found")
    except Exception as e:
        print(f"  Error discovering Tuya devices: {e}")

    print("\n" + "=" * 50)
    print("📋 SUMMARY:")
    print("If no Hubspace devices were found above, they might:")
    print("1. Use a proprietary protocol not supported by these libraries")
    print("2. Be on a different network segment")
    print("3. Require cloud-based control only")
    print("\nFor Hubspace devices, you might need to:")
    print(
        "• Check if they're also compatible with Alexa/Google (might use different protocols)"
    )
    print("• Look for device-specific APIs or unofficial libraries")
    print("• Use network sniffing to reverse engineer the protocol")
    print("• Stick with the Hubspace app for manual control")


if __name__ == "__main__":
    asyncio.run(discover_all_smart_devices())
