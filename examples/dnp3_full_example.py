#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
Complete DNP3 Usage Example

This script demonstrates how to use the various DNP3 components together.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ics.dnp3.dnp3_session import DNP3Session
from ics.dnp3.dnp3_client import DNP3Client
from ics.dnp3.dnp3_read import DNP3Read
from ics.dnp3.safe_dnp3_reader import safe_dnp3_check
from ics.dnp3.safe_dnp3_discover import discover_dnp3


def main():
    print("=" * 60)
    print("ShadowForge DNP3 Full Example")
    print("=" * 60)

    target_ip = "127.0.0.1"
    target_port = 20000

    # 1. Quick reachability check
    print("\n[1] Quick DNP3 Reachability Check")
    check_result = safe_dnp3_check(target_ip, target_port)
    print(f"    Result: {check_result}")

    # 2. Network discovery (limited scope for example)
    print("\n[2] DNP3 Network Discovery (limited to 10 hosts)")
    devices = discover_dnp3(
        network="127.0.0.0/24",
        port=target_port,
        max_hosts=10
    )
    print(f"    Devices found: {devices}")

    # 3. Using DNP3Client (recommended high-level interface)
    print("\n[3] Using DNP3Client (High-Level Interface)")
    with DNP3Client(target_ip, target_port) as client:
        if client.connect():
            print("    ✓ Connected successfully")

            # Read Class 0 data
            class0 = client.read_class_data(class_number=0)
            print(f"    Class 0 data: {class0}")

            # Read Analog Inputs (placeholder)
            analogs = client.read_analog_inputs()
            print(f"    Analog Inputs: {analogs}")
        else:
            print("    ✗ Failed to connect")

    # 4. Lower-level control using DNP3Session + DNP3Read
    print("\n[4] Lower-level control (DNP3Session + DNP3Read)")
    with DNP3Session(target_ip, target_port) as session:
        if session.connected:
            from ics.dnp3.dnp3_read import DNP3Read
            reader = DNP3Read(session)

            result = reader.read_class_0()
            print(f"    Class 0 via DNP3Read: {result}")
        else:
            print("    ✗ Session connection failed")

    print("\n" + "=" * 60)
    print("Example complete. All DNP3 components demonstrated.")
    print("=" * 60)


if __name__ == "__main__":
    main()