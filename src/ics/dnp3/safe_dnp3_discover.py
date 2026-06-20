#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
DNP3 Discovery

Threaded network scanning to find DNP3-capable devices on a target range.
"""

import argparse
import ipaddress
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.logger import get_logger
from utils.config import config
from utils.formatter import print_header, print_section, print_list
from ics.dnp3.safe_dnp3_reader import is_dnp3_reachable

logger = get_logger("DNP3Discover")
DNP3_CFG = config.get("dnp3", {})


def discover_dnp3(network: str = "192.168.0.0/24", port: int = None,
                  max_workers: int = 32, max_hosts: int = 256) -> list:
    """
    Scan a network range for devices that appear to support DNP3.
    """
    port = port or DNP3_CFG.get("default_port", 20000)
    max_workers = max_workers or DNP3_CFG.get("max_workers", 32)
    max_hosts = max_hosts or DNP3_CFG.get("max_hosts", 256)

    logger.info(f"Starting DNP3 discovery on {network} (port {port})")

    try:
        net = ipaddress.ip_network(network, strict=False)
    except ValueError:
        logger.error("Invalid network format")
        return []

    hosts = list(net.hosts())[:max_hosts]
    live_devices = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {
            executor.submit(is_dnp3_reachable, str(ip), port): str(ip)
            for ip in hosts
        }

        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                if future.result():
                    logger.info(f"[+] DNP3 device found: {ip}")
                    live_devices.append(ip)
            except Exception:
                pass

    logger.info(f"Discovery complete. Found {len(live_devices)} device(s)")
    return live_devices


def display_dnp3_discover_results(devices: list, network: str, port: int = None) -> None:
    """Print DNP3 discovery results using the shared CLI formatter."""
    port = port or DNP3_CFG.get("default_port", 20000)

    if devices:
        print_header("DNP3 Discovery Results")
        print_section(f"Network: {network} | Port: {port}")
        print_list("Devices Found", devices)
    else:
        print_header("DNP3 Discovery Results")
        print("[-] No DNP3 devices found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ShadowForge DNP3 Discovery")
    parser.add_argument("--network", default="127.0.0.0/24")
    parser.add_argument("--port", type=int)
    parser.add_argument("--workers", type=int, default=32)
    parser.add_argument("--max-hosts", type=int, default=256)

    args = parser.parse_args()

    devices = discover_dnp3(
        network=args.network,
        port=args.port,
        max_workers=args.workers,
        max_hosts=args.max_hosts
    )

    display_dnp3_discover_results(devices, args.network, args.port)