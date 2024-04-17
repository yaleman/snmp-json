from typing import Any, Callable, Dict, Tuple

from loguru import logger
from snmp_json.config import Config

from pysnmp.hlapi.asyncio.sync.slim import Slim  # type: ignore
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType  # type: ignore
from pysnmp.smi.error import SmiError  # type: ignore


def rename_key(value: str) -> str:
    """strips some stuff"""
    return value.lstrip("if")


def octets_to_bytes(value: str) -> str | int:
    try:
        return int(value) * 8
    except ValueError:
        return value


def update_data(
    config: Config,
    oi: Tuple[str,] | Tuple[str, str],
    data: Dict[str, Any],
    key_alter: Callable[[str], str] = rename_key,
    value_alter: Callable[[str], str | int] = lambda x: x,
) -> None:

    with Slim(2) as slim:
        for ifindex in range(0, config.max_interfaces):
            try:
                errorIndication, errorStatus, errorIndex, varBinds = slim.get(
                    config.community,
                    config.hostname,
                    config.port,
                    # can pull from https://pysnmp.github.io/mibs/asn1/@mib@
                    # ref https://docs.lextudio.com/pysnmp/faq/pass-custom-mib-to-manager
                    ObjectType(
                        ObjectIdentity(*oi, ifindex).addAsn1MibSource(
                            "file:///usr/share/snmp",
                            # "https://mibs.pysnmp.com/asn1/@mib@",
                        )
                    ),
                )
            except SmiError:
                continue

            if errorIndication:
                logger.error(errorIndication)
                continue
            elif errorStatus:
                logger.error(errorStatus)
                continue
            else:
                for varBind in varBinds:
                    key, value = varBind.prettyPrint().split(" = ")
                    key_tail = key.split("::")[-1]
                    key_value = key_tail.split(".")[0]
                    key_index = key_tail.split(".")[-1]
                    if value == "No Such Object currently exists at this OID":
                        continue
                    # print(key_value, key_index, value)
                    if key_index not in data:
                        data[key_index] = {
                            "ifIndex": int(key_index),
                        }
                    data[key_index][key_alter(key_value)] = value_alter(value)
