import json
import sys
from typing import Any, Dict, Optional
import click
from loguru import logger

from snmp_json import octets_to_bytes, update_data
from snmp_json.config import Config


@click.command()
@click.option("--max-interfaces", "-M", default="32", help="Max number of interfaces")
def cli(max_interfaces: Optional[str]) -> None:

    config = Config()
    if config.hostname is None:
        logger.error("No hostname specified!")
        sys.exit(1)
    if config.community is None:
        logger.error("No community specified!")
        sys.exit(1)

    if max_interfaces is not None:
        config.max_interfaces = int(max_interfaces)

    data: Dict[str, Any] = {}

    update_data(config, ("IF-MIB", "ifDescr"), data)
    update_data(config, ("IF-MIB", "ifSpeed"), data, value_alter=int)
    update_data(config, ("IF-MIB", "ifAdminStatus"), data)
    update_data(config, ("IF-MIB", "ifOperStatus"), data)
    update_data(
        config,
        ("IF-MIB", "ifInOctets"),
        data,
        key_alter=lambda x: x.lstrip("if").replace("Octets", "Bytes"),
        value_alter=octets_to_bytes,
    )
    update_data(
        config,
        ("IF-MIB", "ifOutOctets"),
        data,
        key_alter=lambda x: x.lstrip("if").replace("Octets", "Bytes"),
        value_alter=octets_to_bytes,
    )
    update_data(config, ("IF-MIB", "ifAlias"), data)

    for key, value in data.items():
        print(json.dumps(value))


if __name__ == "__main__":
    cli()
