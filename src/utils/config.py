#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
Configuration Management

Handles loading and accessing toolkit configuration.
"""

import json
from pathlib import Path

DEFAULT_CONFIG = {
    "modbus": {
        "default_port": 502,
        "default_timeout": 1.5,
        "max_workers": 32,
        "max_hosts": 256
    },
    "ot_recon": {
        "default_timeout": 1.5,
        "common_ports": [21, 23, 80, 102, 443, 502, 20000, 44818, 47808]
    },
    "dnp3": {
        "default_port": 20000,
        "default_timeout": 2.0,
        "max_workers": 32,
        "max_hosts": 256
    },
    "general": {
        "reports_dir": "reports",
        "log_level": "INFO"
    }
}


def load_config(config_path: str = "config.json") -> dict:
    """Load config from file or return defaults."""
    path = Path(config_path)
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return DEFAULT_CONFIG


def save_config(config: dict, config_path: str = "config.json"):
    """Save config to file."""
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)


# Global config (can be imported elsewhere)
config = load_config()