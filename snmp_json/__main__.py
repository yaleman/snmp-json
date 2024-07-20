from datetime import datetime
import json
import sys
import time
import click
from loguru import logger

from snmp_json import do_action
from snmp_json.config import Config
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType  # type: ignore[import-untyped]


@click.command()
def cli() -> None:

    config = Config()
    if config.debug:
        logger.remove()
        logger.add(sink=sys.stderr, level="DEBUG")
        logger.debug("Debug logging enabled")
        logger.debug("Config: {}", json.dumps(config.model_dump(mode="json")))
    else:
        logger.remove()
        logger.add(sink=sys.stderr, level="INFO")
    if config.hostname is None:
        logger.error("No hostname specified!")
        sys.exit(1)
    if config.community is None:
        logger.error("No community specified!")
        sys.exit(1)

    try:
        if config.interval is not None:
            interval_seconds = float(config.interval)
            logger.debug("Interval set to {} seconds", interval_seconds)
    except ValueError:
        logger.error(
            "Interval value '{}' couldn't be converted to a floating number!",
            config.interval,
        )
        sys.exit(1)

    oi = [
        ObjectType(
            ObjectIdentity(*oid).addAsn1MibSource(
                "file:///usr/share/snmp",
                # "https://mibs.pysnmp.com/asn1/@mib@",
            )
        )
        for oid in [
            ("IF-MIB", "ifAdminStatus"),
            # ("IF-MIB", "ifAlias"),
            # ("IF-MIB", "ifDescr"),
            # ("IF-MIB", "ifInOctets"),
            # ("IF-MIB", "ifOutOctets"),
            # ("IF-MIB", "ifOperStatus"),
            # ("IF-MIB", "ifSpeed"),
        ]
    ]
    while True:
        start_time = datetime.now().timestamp()

        do_action(config, oi)

        if config.interval is None:
            break
        total_time = datetime.now().timestamp() - start_time

        if total_time > interval_seconds:
            logger.warning(
                "Execution time exceeded interval time! {} > {}",
                total_time,
                interval_seconds,
            )
        else:
            time.sleep(interval_seconds - total_time)


if __name__ == "__main__":
    cli()
