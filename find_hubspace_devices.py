#!/usr/bin/env python3.13

"""
Quick test to check if your Hubspace devices might be compatible with other protocols.
This script will help you identify what brand/protocol your Hubspace devices actually use.
"""

import asyncio
import subprocess
import re


def scan_network_devices():
    """Scan for all devices on the network to see what's out there."""
    print("🔍 Scanning network for all devices...")
    print(
        "This might help identify your Hubspace devices by MAC address or manufacturer.\n"
    )

    try:
        # Get network info
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        devices = []

        for line in result.stdout.split("\n"):
            if "(" in line and ")" in line:
                # Extract IP and MAC from arp output
                ip_match = re.search(r"\(([\d.]+)\)", line)
                mac_match = re.search(
                    r"([a-fA-F0-9]{2}:[a-fA-F0-9]{2}:[a-fA-F0-9]{2}:[a-fA-F0-9]{2}:[a-fA-F0-9]{2}:[a-fA-F0-9]{2})",
                    line,
                )

                if ip_match and mac_match:
                    ip = ip_match.group(1)
                    mac = mac_match.group(1)
                    devices.append((ip, mac))

        print("Found devices on your network:")
        for ip, mac in devices:
            # Try to identify manufacturer by MAC prefix
            manufacturer = identify_manufacturer(mac)
            print(f"  📍 {ip} - MAC: {mac} - {manufacturer}")

        print(
            f"\n💡 Look for devices with unfamiliar IPs that might be your Hubspace outlets!"
        )
        print("💡 Check the MAC addresses against known smart device manufacturers.")
        print("💡 Try pinging unknown IPs to see if they respond.")

    except Exception as e:
        print(f"Error scanning network: {e}")


def identify_manufacturer(mac):
    """Try to identify device manufacturer from MAC address prefix."""
    mac_prefixes = {
        "50:c7:bf": "TP-Link",
        "a4:2b:b0": "TP-Link",
        "84:d6:d0": "TP-Link",
        "68:ff:7b": "Tuya/Smart Life",
        "84:f3:eb": "Tuya/Smart Life",
        "1c:90:ff": "Tuya/Smart Life",
        "24:62:ab": "Espressif (ESP32/ESP8266)",
        "3c:71:bf": "Espressif (ESP32/ESP8266)",
        "94:b9:7e": "Espressif (ESP32/ESP8266)",
    }

    prefix = mac[:8].lower()
    return mac_prefixes.get(prefix, "Unknown manufacturer")


if __name__ == "__main__":
    scan_network_devices()

    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS to find your Hubspace devices:")
    print("1. Compare this list with devices you know")
    print("2. Check your router's admin page for device names")
    print("3. Temporarily unplug a Hubspace device and re-run this scan")
    print("4. Check if Hubspace devices appear in Alexa/Google Home")
    print("5. Look up your specific Hubspace device model online")
    print("\n🔧 Alternative approaches:")
    print("• Use IFTTT to create webhooks for Hubspace devices")
    print("• Set up Home Assistant with Hubspace integration")
    print("• Use smart plugs that are Kasa-compatible for Halloween effects")
    print("• Manual control via Hubspace app during the show")
