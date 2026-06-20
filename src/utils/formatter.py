#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
Results Formatter

Provides consistent, colored terminal output for better readability.
"""

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(title: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD} {title}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")


def print_section(title: str):
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}--- {title} ---{Colors.ENDC}")


def print_key_value(key: str, value):
    print(f"  {Colors.OKCYAN}{key}:{Colors.ENDC} {value}")


def print_list(title: str, items: list):
    print(f"\n{Colors.OKGREEN}{title}:{Colors.ENDC}")
    if not items:
        print("  (none found)")
        return
    for item in items:
        if isinstance(item, dict):
            print(f"  {Colors.OKGREEN}•{Colors.ENDC} {item}")
        else:
            print(f"  {Colors.OKGREEN}•{Colors.ENDC} {item}")


def print_success(message: str):
    print(f"{Colors.OKGREEN}[+]{Colors.ENDC} {message}")


def print_warning(message: str):
    print(f"{Colors.WARNING}[!]{Colors.ENDC} {message}")


def print_error(message: str):
    print(f"{Colors.FAIL}[-]{Colors.ENDC} {message}")