#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
Main CLI Launcher

Central command-line interface for all ShadowForge tools.
"""

import argparse
import logging
import sys

from utils.version import __version__, __title__
from utils.formatter import Colors
from utils.logger import get_logger
from utils.config import load_config

from ics.modbus import safe_read_holding_registers, discover_modbus
from ics.modbus.safe_modbus_discover import display_modbus_discover_results
from ics.modbus.modbus_anomaly import ModbusAnomalyDetector
from ics.modbus.modbus_monitor import ModbusMonitor
from ics.modbus.safe_modbus_writer import (
    safe_write_coil,
    safe_write_register,
    enable_writes,
)
from recon.ot_recon import passive_ot_recon, display_ot_recon_results
from ics.dnp3.safe_dnp3_discover import discover_dnp3, display_dnp3_discover_results
from ics.dnp3.safe_dnp3_reader import safe_dnp3_check

logger = get_logger("CLI")


def main():
    parser = argparse.ArgumentParser(
        description=f"{__title__} - Modular tools for safe ICS/OT security research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--config", default="config.json", help="Path to config file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose/debug output")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ============================================
    # Modbus Commands
    # ============================================
    read_p = subparsers.add_parser("modbus-read", help="Read holding registers (safe, read-only)")
    read_p.add_argument("--ip", required=True, help="Target IP address")
    read_p.add_argument("--port", type=int, help="Modbus TCP port")
    read_p.add_argument("--start", type=int, default=0, help="Starting register address")
    read_p.add_argument("--count", type=int, default=5, help="Number of registers to read")

    disc_p = subparsers.add_parser("modbus-discover", help="Discover Modbus devices (threaded)")
    disc_p.add_argument("--network", default="127.0.0.0/24", help="Network range to scan")
    disc_p.add_argument("--port", type=int, help="Modbus TCP port")
    disc_p.add_argument("--workers", type=int, help="Number of threads")
    disc_p.add_argument("--max-hosts", type=int, help="Maximum hosts to scan")
    disc_p.add_argument("--no-report", action="store_true", help="Disable JSON report saving")

    coil_p = subparsers.add_parser("modbus-write-coil", help="Write a single coil (requires confirmation)")
    coil_p.add_argument("--ip", required=True)
    coil_p.add_argument("--port", type=int)
    coil_p.add_argument("--address", type=int, required=True)
    coil_p.add_argument("--value", type=lambda x: x.lower() == "true", required=True)

    reg_p = subparsers.add_parser("modbus-write-register", help="Write a single holding register (requires confirmation)")
    reg_p.add_argument("--ip", required=True)
    reg_p.add_argument("--port", type=int)
    reg_p.add_argument("--address", type=int, required=True)
    reg_p.add_argument("--value", type=int, required=True)

    anom_p = subparsers.add_parser("modbus-anomaly", help="Basic Modbus anomaly detection")
    anom_p.add_argument("--demo", action="store_true", help="Run with demo data")

    mon_p = subparsers.add_parser("modbus-monitor", help="Basic Modbus traffic monitor (simulation mode)")
    mon_p.add_argument("--duration", type=int, default=30, help="How long to monitor (seconds)")
    mon_p.add_argument("--interface", default="any", help="Network interface to monitor")

    # ============================================
    # OT Reconnaissance Commands
    # ============================================
    recon_p = subparsers.add_parser("ot-recon", help="Basic OT reconnaissance (ports + web/HMI)")
    recon_p.add_argument("--target", required=True, help="Target IP address")

    scan_p = subparsers.add_parser("ot-scan", help="Run multiple OT checks together")
    scan_p.add_argument("--target", required=True, help="Target IP address")
    scan_p.add_argument("--modbus", action="store_true", help="Run Modbus discovery")
    scan_p.add_argument("--dnp3", action="store_true", help="Run DNP3 check")
    scan_p.add_argument("--recon", action="store_true", help="Run OT reconnaissance")
    scan_p.add_argument("--all", action="store_true", help="Run all available checks")

    # ============================================
    # DNP3 Commands
    # ============================================
    dnp3_p = subparsers.add_parser("dnp3-check", help="Check DNP3 reachability and connection")
    dnp3_p.add_argument("--ip", required=True, help="Target IP address")
    dnp3_p.add_argument("--port", type=int, default=20000, help="DNP3 port (default: 20000)")

    dnp3_disc_p = subparsers.add_parser("dnp3-discover", help="Discover DNP3 devices on a network")
    dnp3_disc_p.add_argument("--network", default="127.0.0.0/24")
    dnp3_disc_p.add_argument("--port", type=int)
    dnp3_disc_p.add_argument("--workers", type=int)
    dnp3_disc_p.add_argument("--max-hosts", type=int)

    # ============================================
    # Utility Commands
    # ============================================
    list_p = subparsers.add_parser("list", help="List all available commands")

    info_p = subparsers.add_parser("toolkit-info", help="Show information about the ShadowForge Toolkit")

    args = parser.parse_args()

    # Enable verbose mode if requested
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        for name in logging.Logger.manager.loggerDict:
            logging.getLogger(name).setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")

    # Load custom config if provided
    if args.config != "config.json":
        try:
            cfg = load_config(args.config)
            from utils.config import config
            config.clear()
            config.update(cfg)
        except Exception as e:
            logger.error(f"Failed to load config file: {e}")
            sys.exit(1)

    try:
        # ============================================
        # Modbus Command Handlers
        # ============================================
        if args.command == "modbus-read":
            result = safe_read_holding_registers(args.ip, args.port, args.start, args.count)
            print(f"Result: {result}")

        elif args.command == "modbus-discover":
            devices = discover_modbus(
                network=args.network,
                port=args.port,
                max_workers=args.workers,
                max_hosts=args.max_hosts,
                save_report=not args.no_report
            )
            display_modbus_discover_results(devices, args.network, args.port)

        elif args.command == "modbus-write-coil":
            enable_writes()
            success = safe_write_coil(args.ip, args.port, args.address, args.value)
            print(f"Write successful: {success}")

        elif args.command == "modbus-write-register":
            enable_writes()
            success = safe_write_register(args.ip, args.port, args.address, args.value)
            print(f"Write successful: {success}")

        elif args.command == "modbus-anomaly":
            detector = ModbusAnomalyDetector()
            if args.demo:
                for i in range(250):
                    detector.add_observation(function_code=3, register=i % 10)
                anomalies = detector.detect_anomalies()
                print(f"Anomalies detected: {anomalies}")
            else:
                print("Use --demo to run with sample data (real integration coming soon)")

        elif args.command == "modbus-monitor":
            monitor = ModbusMonitor(interface=args.interface)
            monitor.start(duration_seconds=args.duration)

        # ============================================
        # OT Recon Command Handlers
        # ============================================
        elif args.command == "ot-recon":
            result = passive_ot_recon(args.target)
            display_ot_recon_results(result)

        elif args.command == "ot-scan":
            print(f"\n=== Running OT Scan on {args.target} ===\n")

            if args.modbus or args.all:
                print("[*] Running Modbus discovery...")
                devices = discover_modbus(network=f"{args.target}/32", port=5020)
                print(f"    Modbus devices: {devices}\n")

            if args.dnp3 or args.all:
                print("[*] Running DNP3 check...")
                dnp3_result = safe_dnp3_check(args.target)
                print(f"    DNP3 result: {dnp3_result}\n")

            if args.recon or args.all:
                print("[*] Running OT reconnaissance...")
                recon_result = passive_ot_recon(args.target)
                print(f"    Open ports: {recon_result.get('open_ports', [])}\n")

            print("=== OT Scan Complete ===")

        # ============================================
        # DNP3 Command Handlers
        # ============================================
        elif args.command == "dnp3-check":
            from ics.dnp3.dnp3_session import DNP3Session
            logger.info(f"Running DNP3 check on {args.ip}:{args.port or 20000}")
            with DNP3Session(args.ip, args.port or 20000) as session:
                if session.connected:
                    print(f"[+] Successfully connected to DNP3 device at {args.ip}:{args.port or 20000}")
                else:
                    print(f"[-] Failed to connect to DNP3 device at {args.ip}:{args.port or 20000}")

        elif args.command == "dnp3-discover":
            devices = discover_dnp3(
                network=args.network,
                port=args.port,
                max_workers=args.workers,
                max_hosts=args.max_hosts,
            )
            display_dnp3_discover_results(devices, args.network, args.port)

        # ============================================
        # Utility Command Handlers
        # ============================================
        elif args.command == "list":
            print("\nAvailable ShadowForge Commands:\n")
            commands = [
                ("modbus-read", "Read holding registers (safe)"),
                ("modbus-discover", "Discover Modbus devices on a network"),
                ("modbus-write-coil", "Write a coil (requires confirmation)"),
                ("modbus-write-register", "Write a register (requires confirmation)"),
                ("modbus-anomaly", "Run Modbus anomaly detection"),
                ("modbus-monitor", "Monitor Modbus traffic (simulation)"),
                ("ot-recon", "Run OT reconnaissance (ports + web)"),
                ("dnp3-check", "Check if a device supports DNP3"),
                ("dnp3-discover", "Discover DNP3 devices on a network"),
                ("ot-scan", "Run multiple OT checks together"),
                ("list", "Show this list of commands"),
                ("toolkit-info", "Show information about the ShadowForge Toolkit"),
            ]
            for cmd, desc in commands:
                print(f"  {cmd:<20} {desc}")
            print()

        elif args.command == "toolkit-info":
            print(f"\n{Colors.HEADER}{Colors.BOLD}{__title__} v{__version__}{Colors.ENDC}\n")
            print("Available Modules:")
            modules = [
                "Modbus (Reader, Discover, Writer, Anomaly, Monitor)",
                "OT Recon (Ports + Web/HMI)",
                "DNP3 (Reader, Discover, Session, Client, Application, Read)",
                "Assessment Tools (ot-scan, ot_assessment)",
                "Utilities (Logger, Config, Safety, Reporting, HTML Reporter, Formatter)"
            ]
            for m in modules:
                print(f"  • {m}")
            print("\nUse 'python src/auto.py list' to see all CLI commands.\n")

        else:
            parser.print_help()

    except KeyboardInterrupt:
        logger.warning("Operation cancelled by user")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()