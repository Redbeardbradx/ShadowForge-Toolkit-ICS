#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
HTML Reporter

Generates HTML assessment reports from structured result data.
"""

from datetime import datetime
from pathlib import Path


def generate_html_report(data: dict, title: str = "OT Assessment Report") -> str:
    """
    Generate a basic HTML report from assessment data.
    Returns the path to the saved HTML file.
    """
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = reports_dir / f"report_{timestamp}.html"

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; border-bottom: 1px solid #ddd; padding-bottom: 5px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        .section {{ margin-bottom: 30px; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p><strong>Generated:</strong> {datetime.now().isoformat()}</p>
    
    <div class="section">
        <h2>Summary</h2>
        <pre>{data.get('summary', 'No summary available')}</pre>
    </div>

    <div class="section">
        <h2>Full Results</h2>
        <pre>{data}</pre>
    </div>
</body>
</html>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    return str(filename)


if __name__ == "__main__":
    sample_data = {
        "summary": "Assessment completed with 3 open ports and 1 web interface found.",
        "target": "127.0.0.1",
        "timestamp": datetime.now().isoformat()
    }
    path = generate_html_report(sample_data)
    print(f"HTML report saved to: {path}")