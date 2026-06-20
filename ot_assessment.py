#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
Complete OT Assessment Script

Runs combined Modbus, OT Recon, and DNP3 checks with reporting.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from utils.logger import get_logger
from utils.config import config
from utils.formatter import print_header, print_section, print_key_value, print_list
from utils.html_reporter import generate_html_report

from ics.modbus.safe_modbus_discover import discover_modbus
from recon.ot_recon import passive_ot_recon
from ics.dnp3.safe_dnp3_reader import safe_dnp3_check

logger = get_logger("OTAssessment")

MODBUS_SCAN_PORT = 5020
MODBUS_MAX_HOSTS = 5


def _run_modbus_discovery(target: str) -> dict:
    """
    Discover Modbus devices on the target host.

    Args:
        target (str): Target IP address.

    Returns:
        dict: Discovery results or error details.
    """
    print_section("1. Modbus Discovery")
    try:
        devices = discover_modbus(
            network=f"{target}/32",
            port=MODBUS_SCAN_PORT,
            max_hosts=MODBUS_MAX_HOSTS,
        )
        results = {"devices": devices, "count": len(devices)}
        print_list("Modbus Devices Found", devices)
        return results
    except Exception as e:
        logger.error(f"Modbus discovery error: {e}")
        return {"error": str(e)}


def _run_ot_recon(target: str) -> dict:
    """
    Run OT reconnaissance (ports + web interfaces) on the target.

    Args:
        target (str): Target IP address.

    Returns:
        dict: Recon results or error details.
    """
    print_section("2. OT Reconnaissance (Ports + Web Interfaces)")
    try:
        recon = passive_ot_recon(target, save_report=False)
        print_key_value("Open Ports", recon.get("open_port_count", 0))
        print_key_value("Web Interfaces", recon.get("web_interface_count", 0))
        print_list("Open Ports", recon.get("open_ports", []))
        print_list("Web Interfaces", recon.get("web_interfaces", []))
        return recon
    except Exception as e:
        logger.error(f"OT Recon error: {e}")
        return {"error": str(e)}


def _run_dnp3_check(target: str) -> dict:
    """
    Check DNP3 reachability on the target.

    Args:
        target (str): Target IP address.

    Returns:
        dict: DNP3 check results or error details.
    """
    print_section("3. DNP3 Check")
    try:
        dnp3 = safe_dnp3_check(target)
        print_key_value("Reachable", dnp3.get("reachable", False))
        return dnp3
    except Exception as e:
        logger.error(f"DNP3 check error: {e}")
        return {"error": str(e)}


def _save_reports(target: str, results: dict, save_json: bool, save_html: bool) -> None:
    """
    Save assessment results as JSON and/or HTML reports.

    Args:
        target (str): Target IP address.
        results (dict): Full assessment results.
        save_json (bool): Whether to write a JSON report.
        save_html (bool): Whether to write an HTML report.
    """
    if not save_json and not save_html:
        return

    reports_dir = Path(config.get("general", {}).get("reports_dir", "reports"))
    reports_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = target.replace(".", "_")

    if save_json:
        json_file = reports_dir / f"ot_assessment_{safe_target}_{timestamp}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print_key_value("JSON Report", str(json_file))

    if save_html:
        html_file = generate_html_report(results, title=f"OT Assessment - {target}")
        print_key_value("HTML Report", html_file)


def run_ot_assessment(target: str, save_json: bool = True, save_html: bool = True) -> dict:
    """
    Run a full OT assessment on the target.

    Args:
        target (str): Target IP address.
        save_json (bool): Whether to save a JSON report.
        save_html (bool): Whether to save an HTML report.

    Returns:
        dict: Combined assessment results.
    """
    print_header(f"OT Assessment Report - {target}")
    logger.info(f"Starting full OT assessment on {target}")

    results = {
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "modbus": _run_modbus_discovery(target),
        "ot_recon": _run_ot_recon(target),
        "dnp3": _run_dnp3_check(target),
    }

    _save_reports(target, results, save_json, save_html)

    print_header("Assessment Complete")
    return results


def main():
    """Parse CLI arguments and run the OT assessment."""
    parser = argparse.ArgumentParser(
        description="ShadowForge Full OT Assessment",
        epilog="Example: python ot_assessment.py --target 192.168.0.25",
    )
    parser.add_argument("--target", required=True, help="Target IP address")
    parser.add_argument("--no-json", action="store_true", help="Disable JSON report")
    parser.add_argument("--no-html", action="store_true", help="Disable HTML report")

    args = parser.parse_args()

    print("[!] Only run this against systems you own or have explicit written permission to test.\n")
    run_ot_assessment(
        args.target,
        save_json=not args.no_json,
        save_html=not args.no_html,
    )


if __name__ == "__main__":
    main()