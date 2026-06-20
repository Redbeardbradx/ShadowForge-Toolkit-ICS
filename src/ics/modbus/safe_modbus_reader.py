#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
Safe Modbus TCP Reader

Provides safe, read-only access to Modbus holding registers with proper
error handling and connection management.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.logger import get_logger
from utils.config import config
from pymodbus.client import ModbusTcpClient

logger = get_logger("ModbusReader")
MODBUS_CFG = config.get("modbus", {})


def safe_read_holding_registers(ip: str, port: int = None, start_addr: int = 0, count: int = 5):
    """
    Safely read holding registers from a Modbus TCP device.

    Args:
        ip (str): Target device IP address.
        port (int, optional): Modbus TCP port. Defaults to config value.
        start_addr (int): Starting register address.
        count (int): Number of registers to read.

    Returns:
        list or None: List of register values if successful, None on failure.
    """
    port = port or MODBUS_CFG.get("default_port", 502)
    timeout = MODBUS_CFG.get("default_timeout", 1.5)

    client = ModbusTcpClient(host=ip, port=port, timeout=timeout)

    try:
        if not client.connect():
            logger.error(f"Connection failed to {ip}:{port}")
            return None

        logger.info(f"Reading {count} registers from {ip}:{port}")
        result = client.read_holding_registers(address=start_addr, count=count, device_id=1)

        if result.isError():
            logger.error(f"Modbus error: {result}")
            return None

        logger.info(f"Registers: {result.registers}")
        return result.registers

    except Exception as e:
        logger.error(f"Exception: {e}")
        return None

    finally:
        client.close()


if __name__ == "__main__":
    MODBUS_CFG = config.get("modbus", {})

    TARGET_IP = "127.0.0.1"
    TARGET_PORT = MODBUS_CFG.get("default_port", 5020)
    START_ADDRESS = 0
    COUNT = 5

    logger.info("READ-ONLY MODE ENABLED")
    values = safe_read_holding_registers(TARGET_IP, TARGET_PORT, START_ADDRESS, COUNT)

    if values:
        print(f"[+] Result: {values}")
    else:
        print("[-] No response.")