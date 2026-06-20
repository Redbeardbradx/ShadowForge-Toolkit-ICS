#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
Reporting

JSON report generation and persistence for assessment and discovery results.
"""

import json
from datetime import datetime
from pathlib import Path
from utils.config import config


def save_report(data: dict, prefix: str = "report") -> str:
    """
    Save a dictionary as a JSON report in the reports directory.
    Returns the filename.
    """
    reports_dir = Path(config.get("general", {}).get("reports_dir", "reports"))
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = reports_dir / f"{prefix}_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    return str(filename)


def create_report_dict(tool_name: str, target: str, results: dict) -> dict:
    """Create a standardized report structure."""
    return {
        "tool": tool_name,
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "results": results
    }