"""
Main entrypoint for the CLI application.
"""

import sys

from antares.study.version.cli import cli


def main():
    cli(sys.argv[1:])


if __name__ == "__main__":
    main()
