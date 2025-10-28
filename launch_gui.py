"""Convenience launcher for the gem identification GUI."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    """Ensure the repository root is on ``sys.path`` and start the GUI."""

    repo_root = Path(__file__).resolve().parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    from gui import run

    run()


if __name__ == "__main__":
    main()
