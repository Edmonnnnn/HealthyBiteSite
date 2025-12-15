"""
Developer convenience script to start backend (FastAPI) and frontend (static) with one command.

Usage:
  python run_dev.py

Backends binds to 127.0.0.1:8810, frontend to 127.0.0.1:8080.
Stops both processes gracefully on Ctrl+C.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"


def load_env_file(path: Path, env: Dict[str, str]) -> None:
    """Populate env dict with key=value pairs from file if not already set."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if key and key not in env:
            env[key] = value


def start_process(cmd: List[str], cwd: Path, env: Dict[str, str]) -> subprocess.Popen:
    return subprocess.Popen(cmd, cwd=str(cwd), env=env)


def main() -> int:
    backend_env = os.environ.copy()
    load_env_file(BACKEND_DIR / ".env", backend_env)
    backend_env.setdefault("APP_ENV", "dev")
    backend_env.setdefault("APP_PORT", "8810")
    backend_port = backend_env.get("APP_PORT", "8810")

    frontend_env = os.environ.copy()

    backend_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        backend_port,
        "--reload",
    ]

    frontend_cmd = [
        sys.executable,
        "-m",
        "http.server",
        "8080",
        "--bind",
        "127.0.0.1",
    ]

    print("Starting HealthyBite dev stack...")
    print(f"  Backend:  http://127.0.0.1:{backend_port} (FastAPI)")
    print("  Frontend: http://127.0.0.1:8080 (static files)")
    print("Press Ctrl+C to stop both.")

    procs: List[subprocess.Popen] = []
    try:
        procs.append(start_process(backend_cmd, BACKEND_DIR, backend_env))
        procs.append(start_process(frontend_cmd, FRONTEND_DIR, frontend_env))
        # Wait until interrupted
        while True:
            for p in list(procs):
                if p.poll() is not None:
                    raise KeyboardInterrupt
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping processes...")
        for p in procs:
            if p.poll() is None:
                p.terminate()
        for p in procs:
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill()
    return 0


if __name__ == "__main__":
    sys.exit(main())
