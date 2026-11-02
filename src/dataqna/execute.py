import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def run_python(
        code: str,
        csv_path: str,
        timeout: int = 20
) -> str:

    prelude = f"import pandas as pd\ndf = pd.read_csv(r'{csv_path}')\n"

    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "script.py"
        script.write_text(prelude + code, encoding="utf-8")

        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=PROJECT_ROOT,
            )
        except subprocess.TimeoutExpired:
            return f"Error: code took longer than {timeout}s and was stopped."

    if result.returncode != 0:
        return f"Error:\n{result.stderr[-2000:]}"
    return result.stdout[:4000] or "(no output)"