#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
Basic Modbus Traffic Monitor

Provides a simulation-based Modbus traffic monitor with built-in
anomaly detection and session summary reporting.
"""

import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.logger import get_logger
from ics.modbus.modbus_anomaly import ModbusAnomalyDetector

logger = get_logger("ModbusMonitor")


class ModbusMonitor:
    """
    Basic Modbus traffic monitor (currently in simulation mode).

    Records observations, runs anomaly detection, and provides
    a summary at the end of each monitoring session.
    """

    def __init__(self, interface: str = "any"):
        """
        Initialize the monitor.

        Args:
            interface (str): Network interface to monitor (default: "any").
        """
        self.interface = interface
        self.detector = ModbusAnomalyDetector()
        self.running = False
        self.observations = []
        logger.info(f"ModbusMonitor initialized on interface: {interface}")

    def start(self, duration_seconds: int = 30):
        """
        Start monitoring for a set duration.

        Args:
            duration_seconds (int): How long to run the monitor.
        """
        logger.info(f"Starting monitor for {duration_seconds} seconds (simulation mode)")
        self.running = True
        start_time = time.time()

        try:
            while self.running and (time.time() - start_time) < duration_seconds:
                # Simulate traffic
                function_code = 3  # Read Holding Registers (common)
                register = 100 + (len(self.observations) % 20)
                self.detector.add_observation(function_code=function_code, register=register)
                self.observations.append({"function_code": function_code, "register": register})
                time.sleep(0.3)

                anomalies = self.detector.detect_anomalies()
                if anomalies:
                    logger.warning(f"Anomalies: {anomalies}")

        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        finally:
            self.running = False
            self._print_summary()

    def _print_summary(self):
        """Print a summary of the monitoring session."""
        print("\n" + "=" * 50)
        print("Monitoring Session Summary")
        print("=" * 50)
        print(f"Total observations: {len(self.observations)}")

        if self.observations:
            fc_counts = Counter([o["function_code"] for o in self.observations])
            print(f"Function codes seen: {dict(fc_counts)}")

            reg_counts = Counter([o["register"] for o in self.observations])
            print(f"Most accessed registers: {reg_counts.most_common(5)}")

        anomalies = self.detector.detect_anomalies()
        if anomalies:
            print(f"Anomalies detected: {anomalies}")
        else:
            print("No anomalies detected during session.")
        print("=" * 50 + "\n")

    def stop(self):
        """Stop the current monitoring session."""
        self.running = False


if __name__ == "__main__":
    monitor = ModbusMonitor()
    monitor.start(duration_seconds=12)