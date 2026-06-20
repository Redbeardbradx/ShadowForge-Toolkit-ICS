#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
OT Reconnaissance Module

Performs basic reconnaissance on OT targets including:
- Common industrial port scanning
- Web/HMI interface detection
"""

import sys
import socket
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.logger import get_logger
from utils.config import config
from utils.reporting import save_report as persist_report, create_report_dict
from utils.formatter import print_header, print_section, print_key_value, print_list

logger = get_logger("OTRecon")
RECON_CFG = config.get("ot_recon", {})


def check_common_ot_ports(ip: str, timeout: float = None) -> list:
    """
    Scan for common OT/ICS ports and identify services.

    Args:
        ip (str): Target IP address.
        timeout (float, optional): Connection timeout in seconds.

    Returns:
        list: List of open ports with service names.
    """
    timeout = timeout or RECON_CFG.get("default_timeout", 1.5)

    common_ports = {
        502: "Modbus TCP",
        102: "S7comm (Siemens)",
        20000: "DNP3",
        44818: "EtherNet/IP",
        47808: "BACnet",
        80: "HTTP (HMI/Web)",
        443: "HTTPS (HMI/Web)",
        23: "Telnet",
        21: "FTP"
    }

    results = []

    for port, service in common_ports.items():
        try:
            with socket.create_connection((ip, port), timeout=timeout):
                entry = {"port": port, "service": service}
                logger.info(f"[+] {ip}:{port} open ({service})")
                results.append(entry)
        except (socket.timeout, ConnectionRefusedError, OSError):
            pass

    return results


def check_web_interfaces(ip: str, timeout: float = 2.0) -> list:
    """
    Check for common web/HMI interfaces on the target.

    Args:
        ip (str): Target IP address.
        timeout (float): Request timeout in seconds.

    Returns:
        list: List of found web interfaces with status and title.
    """
    import requests
    from requests.exceptions import RequestException

    common_paths = [
        "/",
        "/index.html",
        "/login",
        "/webvisu.htm",
        "/Portal/Portal.mwsl",
        "/main.html"
    ]

    found = []
    headers = {"User-Agent": "ShadowForge-OT-Recon"}

    for path in common_paths:
        url = f"http://{ip}{path}"
        try:
            response = requests.get(url, timeout=timeout, headers=headers, allow_redirects=True)
            if response.status_code == 200:
                title = ""
                if "<title>" in response.text:
                    try:
                        title = response.text.split("<title>")[1].split("</title>")[0].strip()
                    except IndexError:
                        title = "No title"

                entry = {
                    "url": url,
                    "status_code": response.status_code,
                    "title": title
                }
                logger.info(f"[+] Web interface found: {url}")
                found.append(entry)
        except RequestException:
            pass

    return found


def passive_ot_recon(target: str, save_report: bool = True) -> dict:
    """
    Run full OT reconnaissance on a target (ports + web interfaces).

    Args:
        target (str): Target IP address.
        save_report (bool): Whether to save results to file.

    Returns:
        dict: Results including open ports and web interfaces found.
    """
    logger.info(f"Starting OT recon on {target}")

    open_ports = check_common_ot_ports(target)
    web_interfaces = check_web_interfaces(target)

    results = {
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "open_ports": open_ports,
        "open_port_count": len(open_ports),
        "web_interfaces": web_interfaces,
        "web_interface_count": len(web_interfaces)
    }

    if save_report:
        report_data = create_report_dict(
            tool_name="ot_recon",
            target=target,
            results=results
        )
        filename = persist_report(report_data, prefix="ot_recon")
        logger.info(f"Report saved: {filename}")

    logger.info(
        f"Recon complete. Found {len(open_ports)} open ports and "
        f"{len(web_interfaces)} web interfaces"
    )
    return results


def display_ot_recon_results(result: dict) -> None:
    """Print OT recon results using the shared CLI formatter."""
    target = result["target"]
    print_header(f"OT Recon Results for {target}")
    print_key_value("Timestamp", result["timestamp"])
    print_key_value("Open Ports", result["open_port_count"])
    print_key_value("Web Interfaces", result["web_interface_count"])

    print_section("Open Ports")
    print_list("Ports", result["open_ports"])

    print_section("Web Interfaces")
    print_list("Interfaces", result["web_interfaces"])


if __name__ == "__main__":
    target = "127.0.0.1"
    result = passive_ot_recon(target)
    display_ot_recon_results(result)