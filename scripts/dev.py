"""Cross-platform task runner; run with the project's virtual-environment Python."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task", choices=["check", "format", "test"])
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    python = sys.executable
    commands = {
        "test": [[python, "-m", "pytest"]],
        "format": [
            [python, "-m", "ruff", "check", "--fix", "."],
            [python, "-m", "ruff", "format", "."],
        ],
        "check": [
            [python, "-m", "ruff", "check", "."],
            [python, "-m", "ruff", "format", "--check", "."],
            [python, "-m", "pytest"],
            [
                shutil.which("npm.cmd") or shutil.which("npm") or "npm",
                "--prefix",
                "frontend",
                "run",
                "typecheck",
            ],
            [
                shutil.which("npm.cmd") or shutil.which("npm") or "npm",
                "--prefix",
                "frontend",
                "run",
                "build",
            ],
        ],
    }
    for command in commands[args.task]:
        subprocess.run(command, cwd=root, check=True)


if __name__ == "__main__":
    main()
