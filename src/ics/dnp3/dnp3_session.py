#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
DNP3 Session Management

Handles TCP connection, send/receive, and basic session lifecycle for DNP3 devices.
"""

import sys
import socket
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.logger import get_logger

logger = get_logger("DNP3Session")


class DNP3Session:
    """
    Foundation class for DNP3 session handling.
    Current capabilities:
    - TCP connection management
    - Basic send/receive methods
    - Context manager support

    Future capabilities will include:
    - Full DNP3 handshaking
    - Reading analog/binary/counter data
    - Sending control commands
    """

    def __init__(self, ip: str, port: int = 20000, timeout: float = 5.0):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.connected = False
        self.socket = None
        logger.info(f"DNP3Session created for {ip}:{port}")

    def connect(self) -> bool:
        try:
            self.socket = socket.create_connection((self.ip, self.port), timeout=self.timeout)
            self.connected = True
            logger.info(f"[+] Connected to {self.ip}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Connection failed to {self.ip}:{self.port}: {e}")
            self.connected = False
            return False

    def disconnect(self):
        if self.socket:
            try:
                self.socket.close()
                logger.info(f"Disconnected from {self.ip}:{self.port}")
            except Exception as e:
                logger.error(f"Disconnect error: {e}")
        self.connected = False
        self.socket = None

    def send(self, data: bytes) -> bool:
        """Send raw bytes over the DNP3 connection."""
        if not self.connected or not self.socket:
            logger.error("Cannot send - not connected")
            return False
        try:
            self.socket.sendall(data)
            logger.debug(f"Sent {len(data)} bytes to {self.ip}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Send error: {e}")
            return False

    def receive(self, buffer_size: int = 4096) -> bytes:
        """Receive raw bytes from the DNP3 connection."""
        if not self.connected or not self.socket:
            logger.error("Cannot receive - not connected")
            return b""
        try:
            data = self.socket.recv(buffer_size)
            logger.debug(f"Received {len(data)} bytes from {self.ip}:{self.port}")
            return data
        except Exception as e:
            logger.error(f"Receive error: {e}")
            return b""

    def read_analog_inputs(self) -> list:
        logger.warning("read_analog_inputs() not yet implemented")
        return []

    def read_binary_inputs(self) -> list:
        logger.warning("read_binary_inputs() not yet implemented")
        return []

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False


if __name__ == "__main__":
    with DNP3Session("127.0.0.1", 20000) as session:
        print(f"Connected: {session.connected}")