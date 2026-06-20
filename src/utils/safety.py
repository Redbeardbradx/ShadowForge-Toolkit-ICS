#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
Safety Controls

Confirmation prompts and safety interlocks for write and disruptive operations.
"""

def confirm_action(action_description: str) -> bool:
    """Force explicit confirmation before any write/disruptive action."""
    print(f"\n[!] SAFETY WARNING: {action_description}")
    response = input("Type 'YES' to continue: ").strip()
    return response == "YES"


def is_lab_only() -> bool:
    """Placeholder for future lab network checks."""
    return True