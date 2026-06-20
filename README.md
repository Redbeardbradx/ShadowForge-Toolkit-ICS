# ShadowForge Toolkit (ICS/OT Edition)

A modular Python toolkit for safe Industrial Control Systems (ICS) and Operational Technology (OT) security research and assessment.

## Purpose

Built as a portfolio and learning project to combine real-world operational experience with technical security skills. The toolkit focuses on safe protocol interaction, responsible discovery, and basic defensive capabilities in OT environments.

## Quick Start

```bash
git clone https://github.com/redbeardbradx/ShadowForge-Toolkit-ICS.git
cd ShadowForge-Toolkit-ICS

python -m venv venv
.\venv\Scripts\Activate.ps1          # Windows
# source venv/bin/activate          # Linux/macOS

pip install -r requirements.txt
cp config.json.example config.json   # Linux/macOS
# copy config.json.example config.json   # Windows

python src/auto.py list
```

## Why This Toolkit Matters

Most penetration testers come from pure IT backgrounds. This toolkit was built by someone with over 20 years of hands-on experience in heavy equipment, construction, and industrial processes — giving it a practical perspective on how security applies to real operational environments.

## Current Features

- **Modbus Suite**: Reader, Discover, Writer (with safety controls), Anomaly Detector, Traffic Monitor
- **OT Recon**: Port scanning + Web/HMI interface detection
- **DNP3 Suite**: Reader, Discover, Session handling, Client, Application layer, Read interface
- **Assessment Tools**: Combined `ot-scan` and full `ot_assessment.py` (with JSON + HTML reporting)
- **Utilities**: Centralized logging, configuration, safety interlocks, colored output formatting
- **CLI**: Feature-rich command-line interface with verbose mode and helpful commands

## Current Status

This toolkit is actively being developed as a learning and portfolio project.  
Core modules (Modbus, DNP3, OT Recon, Assessment tools) are functional and usable.

## Safety Notice

All tools are designed with safety in mind:

- Read-only operations by default where possible
- Hard limits and confirmation prompts for any write operations
- Intended for lab and authorized assessment use only

**Never run these tools against production ICS environments without explicit written permission.**

## Project Structure

```
src/
├── ics/
│   ├── modbus/          # Modbus tools + anomaly detection + monitoring
│   └── dnp3/            # Full DNP3 module suite
├── recon/               # OT reconnaissance (ports + web/HMI)
├── utils/               # Shared utilities (logger, config, reporting, etc.)
└── auto.py              # Main CLI entry point

ot_assessment.py         # Complete assessment script with reporting
examples/                # Usage examples
```

## Usage Examples

### Full OT Assessment

```bash
python ot_assessment.py --target 192.168.0.25
```

### Using the CLI

```bash
python src/auto.py list
python src/auto.py toolkit-info
python src/auto.py modbus-discover --network 192.168.0.0/24
python src/auto.py ot-recon --target 192.168.0.25
```

## Author

**Brad Malmgren**  
Heavy Equipment Operator | ICS/OT Security Enthusiast  
Utah, USA  
[LinkedIn](https://www.linkedin.com/in/brad-lee-malmgren-55bb8b17)

This toolkit is developed as a personal learning and portfolio project.

## License

MIT License — see [LICENSE](LICENSE). For educational and authorized security research use only.