"""One-time project-local setup. Uses only Python's standard library."""
from pathlib import Path
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parents[1]


def main():
    if not (3, 10) <= sys.version_info[:2] <= (3, 13):
        print("Use Python 3.12 (recommended), or Python 3.10-3.13. Install it from python.org.")
        return 1
    try:
        import tkinter  # noqa: F401
    except ImportError:
        print("Tkinter is missing. On Windows, modify your Python installation and enable Tcl/Tk.")
        print("On Ubuntu/Debian, install python3-tk and python3-venv first.")
        return 1
    executable = ROOT / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    try:
        if not executable.exists():
            print("Creating an isolated .venv in the project folder...", flush=True)
            venv.EnvBuilder(with_pip=True).create(ROOT / ".venv")
        result = subprocess.run([str(executable), "-m", "pip", "--version"], capture_output=True)
        if result.returncode:
            subprocess.run([str(executable), "-m", "ensurepip", "--upgrade"], check=True)
        print("Installing libraries and the English model. Internet is needed for this step.", flush=True)
        subprocess.run([str(executable), "-m", "pip", "install", "-r", str(ROOT / "requirements-model.txt")], cwd=ROOT, check=True)
        subprocess.run([str(executable), str(ROOT / "scripts" / "verify_setup.py")], cwd=ROOT, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Setup could not finish: {exc}")
        print("Check internet access, your Python version and folder permissions, then run setup again.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
