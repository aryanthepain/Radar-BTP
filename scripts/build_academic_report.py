"""
DEPRECATED: scripts/build_academic_report.py has been deprecated per Decision D-12.
docs/index.html is directly maintained as the single authoritative source of truth for the
publication-grade academic thesis portal to eliminate split-brain drift and indirection.
"""

import sys

def main():
    print("DEPRECATION NOTICE: scripts/build_academic_report.py is deprecated per Decision D-12.")
    print("docs/index.html is the single authoritative source of truth.")
    print("Please edit docs/index.html directly and run pytest tests/test_academic_website.py to verify.")
    sys.exit(0)

if __name__ == "__main__":
    main()
