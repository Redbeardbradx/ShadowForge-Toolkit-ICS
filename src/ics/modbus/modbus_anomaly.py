#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
Modbus Anomaly Detector

Tracks Modbus observations and detects basic anomalies such as:
- High volume of traffic
- Unusual function code distribution
- Repeated access to the same registers
"""

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.logger import get_logger

logger = get_logger("ModbusAnomaly")


class ModbusAnomalyDetector:
    """
    Simple anomaly detector for Modbus traffic.

    Use this class to record observations and check for suspicious patterns.
    """

    def __init__(self):
        self.function_counts = defaultdict(int)
        self.register_access = defaultdict(int)
        self.total_observations = 0
        logger.info("ModbusAnomalyDetector initialized")

    def add_observation(self, function_code: int, register: int = None):
        """
        Record a new Modbus observation.

        Args:
            function_code (int): Modbus function code used.
            register (int, optional): Register address accessed.
        """
        self.function_counts[function_code] += 1
        if register is not None:
            self.register_access[register] += 1
        self.total_observations += 1

    def detect_anomalies(self) -> list:
        """
        Run basic anomaly detection rules on recorded observations.

        Returns:
            list: List of detected anomaly descriptions (empty if none found).
        """
        anomalies = []

        if self.total_observations == 0:
            return anomalies

        # Rule 1: High volume of observations
        if self.total_observations > 200:
            anomalies.append("High observation volume detected")

        # Rule 2: Unusual function code distribution
        if self.function_counts:
            most_common = max(self.function_counts.values())
            if most_common > self.total_observations * 0.7:
                anomalies.append("Dominant function code usage detected")

        # Rule 3: Repeated access to same registers
        if self.register_access:
            max_access = max(self.register_access.values())
            if max_access > 50:
                anomalies.append("Repeated register access detected")

        if anomalies:
            logger.warning(f"Anomalies detected: {anomalies}")
        else:
            logger.info("No anomalies detected")

        return anomalies

    def reset(self):
        """Clear all recorded observations and counts."""
        self.function_counts.clear()
        self.register_access.clear()
        self.total_observations = 0
        logger.info("Anomaly detector reset")


if __name__ == "__main__":
    detector = ModbusAnomalyDetector()

    # Simulate some traffic
    for i in range(250):
        detector.add_observation(function_code=3, register=i % 10)

    anomalies = detector.detect_anomalies()
    print(f"Anomalies: {anomalies}")