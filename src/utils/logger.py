#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
Shared Logger Utility

Centralized logging for consistent output across all modules.
"""

import logging

def get_logger(name="ShadowForge"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger