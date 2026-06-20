#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
DNP3 Objects

Object group and variation definitions for DNP3 data types.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.logger import get_logger

logger = get_logger("DNP3Objects")


class DNP3Object:
    """
    Base class for DNP3 data objects.
    Future versions will support specific object groups and variations.
    """

    def __init__(self, group: int, variation: int, data: bytes = b""):
        self.group = group
        self.variation = variation
        self.data = data
        logger.debug(f"DNP3Object created: Group {group}, Variation {variation}")

    def __repr__(self):
        return f"DNP3Object(Group={self.group}, Variation={self.variation})"


class AnalogInput(DNP3Object):
    """Placeholder for Analog Input objects (Group 30)."""

    def __init__(self, index: int, value: float = 0.0):
        super().__init__(group=30, variation=1)
        self.index = index
        self.value = value
        logger.debug(f"AnalogInput created: Index={index}, Value={value}")


class BinaryInput(DNP3Object):
    """Placeholder for Binary Input objects (Group 1)."""

    def __init__(self, index: int, value: bool = False):
        super().__init__(group=1, variation=1)
        self.index = index
        self.value = value
        logger.debug(f"BinaryInput created: Index={index}, Value={value}")


if __name__ == "__main__":
    analog = AnalogInput(index=0, value=123.45)
    binary = BinaryInput(index=5, value=True)

    print(analog)
    print(binary)