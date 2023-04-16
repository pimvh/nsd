import argparse
import logging
import subprocess
import sys

SERIAL_MARKER = "; Serial"

logging.basicConfig(level="INFO")
logger = logging.getLogger()


def grep_zone_serial(nsd_directory: str, domain: str):
    """find DNS serial based on marker"""

    try:
        grepper = subprocess.run(
            f'grep -i "{SERIAL_MARKER}" "{nsd_directory}/{domain}.zone"',
            capture_output=True,
            shell=True,
            check=True,
        )

        serial = grepper.stdout.decode("utf-8").split(";")[0].strip()
        return serial

    except subprocess.CalledProcessError as e:
        logger.exception("Error grepping zonefile: %s", e)
        sys.exit(1)


def main():
    """main function to get a serial from a NSD DNS zonefile"""
    parser = argparse.ArgumentParser()

    parser.add_argument("nsd_directory", help="directory where nsd lives")
    parser.add_argument("domain", help="domain the zonefile is for")

    args = parser.parse_args()

    print(grep_zone_serial(args.nsd_directory, args.domain))


if __name__ == "__main__":
    main()
