import subprocess
import sys
import re
import tempfile
from pathlib import Path
from collections.abc import Callable
from dataclasses import dataclass

PROJECT_ROOT = Path(__file__).resolve().parents[2]

@dataclass
class RunResult:
    ok: bool
    stdout: str
    stderr: str
    timed_out: bool = False

def _extract_python(
        code: str
) -> str | None:
    
    if not code:
        return None

    # Complete fenced block
    m = re.search(r"```(?:python|py)?[ \t]*\r?\n(.*?)```", code, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # Opening fence but no closing fence (truncated reply)
    m = re.search(r"```(?:python|py)?[ \t]*\r?\n(.*)", code, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    return None

def _run_once(
        code: str,
        csv_path: Path,
        timeout: int = 20
) -> RunResult:

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
            return RunResult(
                ok = False,
                stdout = "",
                stderr = f"Error: code took longer than {timeout}s and was stopped.",
                timed_out=True
            )
        return RunResult(
            ok = result.returncode == 0,
            stdout = result.stdout[:4000],
            stderr = result.stderr[:4000],
        )




def run_python(
        code: str,
        csv_path: Path,
        timeout: int = 20,
        max_retries: int = 1,
        fix: Callable[[str, RunResult, int], str] | None = None
) -> tuple[str, str]:
    
    code = _extract_python(code) or code.strip()
    res = _run_once(code, csv_path, timeout)

    for attempt in range(max_retries + 1):
        if res.ok:
            return(res.stdout.strip() or "(no output)"), code

        if attempt == max_retries or fix is None:
            break

        raw = fix(code, res, timeout) or ""
        new_code = _extract_python(raw) or raw.strip()
        if not new_code or new_code == code:
            break

        code = new_code
        res = _run_once(code, csv_path, timeout)

    return f"Error:\n{res.stderr or '(timeout)'}", code