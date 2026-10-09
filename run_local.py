"""Start a local-only server: uv run python run_local.py"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the portfolio on localhost.")
    parser.add_argument("--port", type=int, default=8501, help="Local port (default: 8501)")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")

    # These flags apply only to this process; Community Cloud uses resume_app.py.
    command = [
        sys.executable, "-m", "streamlit", "run", str(ROOT / "resume_app.py"),
        "--server.address=127.0.0.1",
        "--browser.serverAddress=localhost",
        f"--server.port={args.port}",
        f"--browser.serverPort={args.port}",
    ]
    process = subprocess.Popen(command, cwd=ROOT)
    try:
        return process.wait()
    except KeyboardInterrupt:
        # Ctrl+C also reaches the child on normal terminals; terminate if needed.
        if process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
