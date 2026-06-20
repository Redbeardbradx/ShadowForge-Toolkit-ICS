# ShadowForge Toolkit - Examples

This folder contains example scripts that demonstrate how to use different parts of the ShadowForge Toolkit.

## Available Examples

- `dnp3_full_example.py` — Shows how to use the full DNP3 module suite together (recommended starting point for DNP3)
- `dnp3_example.py` — Basic DNP3 usage example (reachability check, discovery, and client)

## How to Run

```bash
cd ..
python -m venv venv
source venv/bin/activate          # or .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt

python examples/dnp3_full_example.py
```

## Notes

These examples are meant for learning and demonstration only.
Always run them against systems you own or have explicit permission to test.