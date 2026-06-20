#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
DNP3 Reader

Safe DNP3 reachability checks with JSON report generation.
"""

import sys
import socket
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.logger import get_logger
from utils.config import config
from utils.reporting import save_report as persist_report, create_report_dict

logger = get_logger("DNP3")
DNP3_CFG = config.get("dnp3", {})


def is_dnp3_reachable(ip: str, port: int = None, timeout: float = None) -> bool:
    port = port or DNP3_CFG.get("default_port", 20000)
    timeout = timeout or DNP3_CFG.get("default_timeout", 2.0)

    try:
        with socket.create_connection((ip, port), timeout=timeout):
            logger.info(f"[+] {ip}:{port} is reachable")
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def safe_dnp3_check(ip: str, port: int = None, save_report: bool = True) -> dict:
    port = port or DNP3_CFG.get("default_port", 20000)

    logger.info(f"Checking DNP3 on {ip}:{port}")

    result = {
        "ip": ip,
        "port": port,
        "reachable": False,
        "protocol": "DNP3",
        "note": "Basic TCP reachability check only. Full DNP3 support not yet implemented."
    }

    if is_dnp3_reachable(ip, port):
        result["reachable"] = True
        logger.info(f"[+] {ip}:{port} appears to support DNP3")

    if save_report:
        report_data = create_report_dict(
            tool_name="dnp3_check",
            target=f"{ip}:{port}",
            results=result
        )
        filename = persist_report(report_data, prefix="dnp3_check")
        logger.info(f"Report saved: {filename}")

    return result


if __name__ == "__main__":
    result = safe_dnp3_check("127.0.0.1")
    print(result)