#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
High-Level DNP3 Client

User-friendly interface for common DNP3 operations.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.logger import get_logger
from ics.dnp3.dnp3_master import DNP3Master
from ics.dnp3.dnp3_parser import DNP3Parser

logger = get_logger("DNP3Client")


class DNP3Client:
    """
    High-level DNP3 client interface.
    This class provides a simpler way to interact with DNP3 devices.
    It will become more powerful as DNP3Master and DNP3Parser are expanded.
    """

    def __init__(self, ip: str, port: int = 20000):
        self.ip = ip
        self.port = port
        self.master = DNP3Master(ip, port)
        logger.info(f"DNP3Client created for {ip}:{port}")

    def connect(self) -> bool:
        """Connect to the DNP3 device."""
        return self.master.connect()

    def disconnect(self):
        """Disconnect from the DNP3 device."""
        self.master.disconnect()

    def read_class_data(self, class_number: int = 0) -> dict:
        """
        Placeholder for reading class data (Class 0, 1, 2, or 3).
        Will be implemented in future versions.
        """
        logger.warning(f"read_class_data(class {class_number}) not yet implemented")
        return {}

    def get_device_status(self) -> dict:
        """
        Placeholder for retrieving device status / health information.
        Will be implemented in future versions.
        """
        logger.warning("get_device_status() not yet implemented")
        return {}

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False


if __name__ == "__main__":
    client = DNP3Client("127.0.0.1", 20000)
    print("DNP3Client created (placeholder)")