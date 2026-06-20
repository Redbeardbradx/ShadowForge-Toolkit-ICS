#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
Safe Modbus TCP Writer

Write operations with multiple safety confirmation layers.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.logger import get_logger
from utils.config import config
from utils.safety import confirm_action
from pymodbus.client import ModbusTcpClient

logger = get_logger("ModbusWriter")
MODBUS_CFG = config.get("modbus", {})

# Global safety switch - writes are disabled by default
WRITES_ENABLED = False


def enable_writes():
    """Enable write operations (must be called intentionally)."""
    global WRITES_ENABLED
    WRITES_ENABLED = True
    logger.warning("WRITE OPERATIONS HAVE BEEN ENABLED")


def safe_write_coil(ip: str, port: int, address: int, value: bool) -> bool:
    """
    Safely write a single coil with multiple confirmation layers.
    """
    if not WRITES_ENABLED:
        logger.error("Writes are currently disabled. Call enable_writes() first.")
        return False

    client = ModbusTcpClient(host=ip, port=port, timeout=3)

    try:
        if not client.connect():
            logger.error(f"Connection failed to {ip}:{port}")
            return False

        # Final confirmation
        action = f"Write coil {address} = {value} on {ip}:{port}"
        if not confirm_action(action):
            logger.warning("Write operation cancelled by user")
            return False

        logger.warning(f"Writing coil {address} = {value} on {ip}:{port}")
        result = client.write_coil(address=address, value=value, device_id=1)

        if result.isError():
            logger.error(f"Write failed: {result}")
            return False

        logger.info(f"Successfully wrote coil {address} = {value}")
        return True

    except Exception as e:
        logger.error(f"Exception during write: {e}")
        return False

    finally:
        client.close()


def safe_write_register(ip: str, port: int, address: int, value: int) -> bool:
    """
    Safely write a single holding register with confirmation.
    """
    if not WRITES_ENABLED:
        logger.error("Writes are currently disabled. Call enable_writes() first.")
        return False

    client = ModbusTcpClient(host=ip, port=port, timeout=3)

    try:
        if not client.connect():
            logger.error(f"Connection failed to {ip}:{port}")
            return False

        action = f"Write register {address} = {value} on {ip}:{port}"
        if not confirm_action(action):
            logger.warning("Write operation cancelled by user")
            return False

        logger.warning(f"Writing register {address} = {value} on {ip}:{port}")
        result = client.write_register(address=address, value=value, device_id=1)

        if result.isError():
            logger.error(f"Write failed: {result}")
            return False

        logger.info(f"Successfully wrote register {address} = {value}")
        return True

    except Exception as e:
        logger.error(f"Exception during write: {e}")
        return False

    finally:
        client.close()


if __name__ == "__main__":
    print("[!] This module contains write functions with safety interlocks.")
    print("[!] Writes are disabled by default.")