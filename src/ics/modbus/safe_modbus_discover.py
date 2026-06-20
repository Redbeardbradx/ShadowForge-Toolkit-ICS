#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
Safe Modbus Network Discovery

Performs threaded, rate-limited discovery of Modbus TCP devices
across a network range with safety controls and reporting.
"""

import sys
import argparse
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.logger import get_logger
from utils.config import config
from utils.formatter import print_header, print_section, print_list
from pymodbus.client import ModbusTcpClient

logger = get_logger("ModbusDiscover")

# Load settings from config
MODBUS_CFG = config.get("modbus", {})


def is_modbus_device(ip: str, port: int = None, timeout: float = None) -> bool:
    """
    Check if a host is running a Modbus TCP service.

    Args:
        ip (str): IP address to check.
        port (int, optional): Modbus port. Defaults to config.
        timeout (float, optional): Connection timeout in seconds.

    Returns:
        bool: True if device responds to Modbus, False otherwise.
    """
    port = port or MODBUS_CFG.get("default_port", 502)
    timeout = timeout or MODBUS_CFG.get("default_timeout", 1.5)

    client = ModbusTcpClient(host=ip, port=port, timeout=timeout)
    try:
        if client.connect():
            result = client.read_holding_registers(address=0, count=1, device_id=1)
            return not result.isError()
    except Exception:
        return False
    finally:
        client.close()
    return False


def discover_modbus(network: str = "192.168.0.0/24", port: int = None,
                    max_workers: int = None, max_hosts: int = None,
                    save_report: bool = True) -> list:
    """
    Discover Modbus devices on a given network range.

    Args:
        network (str): Network in CIDR notation (e.g. "192.168.0.0/24").
        port (int, optional): Modbus TCP port.
        max_workers (int, optional): Number of threads to use.
        max_hosts (int, optional): Maximum number of hosts to scan.
        save_report (bool): Whether to save results as JSON.

    Returns:
        list: List of IP addresses that responded as Modbus devices.
    """
    port = port or MODBUS_CFG.get("default_port", 502)
    max_workers = max_workers or MODBUS_CFG.get("max_workers", 32)
    max_hosts = max_hosts or MODBUS_CFG.get("max_hosts", 256)

    logger.info(f"Scanning {network} on port {port}")

    try:
        net = ipaddress.ip_network(network, strict=False)
    except ValueError:
        logger.error("Invalid network")
        return []

    hosts = list(net.hosts())[:max_hosts]
    live_devices = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {
            executor.submit(is_modbus_device, str(ip), port): str(ip)
            for ip in hosts
        }

        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                if future.result():
                    logger.info(f"[+] Found: {ip}")
                    live_devices.append(ip)
            except Exception:
                pass

    logger.info(f"Found {len(live_devices)} device(s)")

    if save_report and live_devices:
        from utils.reporting import save_report, create_report_dict

        report_data = create_report_dict(
            tool_name="modbus_discover",
            target=network,
            results={"devices": live_devices, "count": len(live_devices)}
        )
        filename = save_report(report_data, prefix="modbus_discover")
        logger.info(f"Report saved: {filename}")

    return live_devices


def display_modbus_discover_results(devices: list, network: str, port: int = None) -> None:
    """Print Modbus discovery results using the shared CLI formatter."""
    port = port or MODBUS_CFG.get("default_port", 502)

    if devices:
        print_header("Modbus Discovery Results")
        print_section(f"Network: {network} | Port: {port}")
        print_list("Devices Found", devices)
    else:
        print_header("Modbus Discovery Results")
        print("[-] No Modbus devices found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--network", default="127.0.0.0/24")
    parser.add_argument("--port", type=int)
    parser.add_argument("--workers", type=int)
    parser.add_argument("--max-hosts", type=int)
    parser.add_argument("--no-report", action="store_true")

    args = parser.parse_args()

    devices = discover_modbus(
        network=args.network,
        port=args.port,
        max_workers=args.workers,
        max_hosts=args.max_hosts,
        save_report=not args.no_report
    )
    display_modbus_discover_results(devices, args.network, args.port)