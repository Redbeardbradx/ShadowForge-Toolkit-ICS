#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
DNP3 Usage Example
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ics.dnp3.dnp3_client import DNP3Client
from ics.dnp3.safe_dnp3_reader import safe_dnp3_check
from ics.dnp3.safe_dnp3_discover import discover_dnp3


def main():
    print("=== ShadowForge DNP3 Example ===\n")

    target = "127.0.0.1"

    # 1. Single device check
    print("[1] Checking single device...")
    result = safe_dnp3_check(target, 20000)
    print(f"    Result: {result}\n")

    # 2. Network discovery (limited for example)
    print("[2] Discovering DNP3 devices on 127.0.0.0/24...")
    devices = discover_dnp3(network="127.0.0.0/24", port=20000, max_hosts=10)
    print(f"    Devices found: {devices}\n")

    # 3. Using DNP3Client (high-level interface)
    print("[3] Using DNP3Client...")
    with DNP3Client(target, 20000) as client:
        if client.connect():
            print("    Connected successfully (placeholder behavior)")
            status = client.get_device_status()
            print(f"    Device status: {status}")
        else:
            print("    Failed to connect")


if __name__ == "__main__":
    main()