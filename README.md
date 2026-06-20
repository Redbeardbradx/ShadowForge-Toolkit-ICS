# ShadowForge Toolkit (ICS/OT Edition)

A modular Python toolkit for safe Industrial Control Systems (ICS) and Operational Technology (OT) security research and assessment.

## Quick Start

```bash
git clone https://github.com/redbeardbradx/ShadowForge-Toolkit-ICS.git
cd ShadowForge-Toolkit-ICS

python -m venv venv
.\venv\Scripts\Activate.ps1          # Windows
# source venv/bin/activate          # Linux/macOS

pip install -r requirements.txt

python src/auto.py list
```

## Purpose

Built as a portfolio project to combine real-world operational experience with technical security skills. The toolkit focuses on:

- Safe protocol interaction (Modbus TCP, DNP3)
- Rate-limited and responsible discovery
- OT reconnaissance (ports + web/HMI interfaces)
- Basic anomaly detection and monitoring
- Clean, auditable, and well-structured Python code

## Why This Toolkit Matters for OT/ICS Security

Most penetration testers come from pure IT backgrounds. This toolkit was built by someone with 20+ years of hands-on experience in heavy equipment, construction, and industrial processes — giving it a unique perspective on how security applies to real operational environments.

## Current Features

- **Modbus Suite**: Reader, Discover, Writer (with safety controls), Anomaly Detector, Traffic Monitor
- **OT Recon**: Port scanning + Web/HMI interface detection
- **DNP3 Suite**: Reader, Discover, Session handling, Client, Application layer, Read interface
- **Assessment Tools**: `ot-scan` (combined checks) and full `ot_assessment.py` (with JSON + HTML reports)
- **Utilities**: Centralized logging, configuration, safety interlocks, reporting, and colored output formatting
- **CLI**: Rich command-line interface with verbose mode, config support, and helpful commands

## Installation

```bash
git clone https://github.com/Redbeardbradx/ShadowForge-Toolkit-ICS.git
cd ShadowForge-Toolkit-ICS

python -m venv venv
source venv/bin/activate          # Linux/macOS
# .\venv\Scripts\Activate.ps1   # Windows

pip install -r requirements.txt
cp config.json.example config.json   # Linux/macOS
# copy config.json.example config.json   # Windows
```

## Usage Examples

### Run a Full OT Assessment

```bash
python ot_assessment.py --target 192.168.0.25
```

This will:

- Discover Modbus devices
- Run OT reconnaissance (ports + web interfaces)
- Check for DNP3
- Generate both JSON and HTML reports

### Use Individual Commands via CLI

```bash
python src/auto.py list                    # Show all available commands
python src/auto.py toolkit-info            # Show toolkit information
python src/auto.py modbus-discover --network 192.168.0.0/24 --port 502
python src/auto.py ot-recon --target 192.168.0.25
python src/auto.py dnp3-discover --network 192.168.0.0/24
```

## Safety Notice

All tools are designed with safety in mind:

- Read-only operations by default where possible
- Hard limits and confirmation prompts for write operations
- Intended for lab and authorized assessment use only

**Never run these tools against production ICS environments without explicit written permission.**

## Project Structure

```
src/
├── ics/
│   ├── modbus/          # Modbus tools + anomaly + monitor
│   └── dnp3/            # Full DNP3 module suite
├── recon/               # OT reconnaissance
├── utils/               # Shared utilities (logger, config, reporting, etc.)
└── auto.py              # Main CLI entry point

ot_assessment.py         # Complete assessment script
examples/                # Usage examples
```

## Current Status

This toolkit is actively being developed as a learning and portfolio project.  
Core features (Modbus, DNP3, OT Recon, Assessment tools) are functional.

## Author

**Brad Malmgren**  
Heavy Equipment Operator | ICS/OT Security Enthusiast  
[LinkedIn](https://www.linkedin.com/in/brad-lee-malmgren-55bb8b17)

## License

MIT License — see [LICENSE](LICENSE). For educational and authorized security research use only.