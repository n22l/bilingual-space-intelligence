"""Backward-compatible command for the Technical Research Engine."""
import sys

sys.dont_write_bytecode = True

from research_search import main


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
