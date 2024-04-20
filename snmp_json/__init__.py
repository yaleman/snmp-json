import asyncio
import json
from typing import Any, Callable, Dict, List, Tuple

from loguru import logger
from snmp_json.config import Config

from pysnmp.hlapi.asyncio import bulkWalkCmd, UdpTransportTarget, ContextData  # type: ignore
from pysnmp.entity.engine import SnmpEngine  # type: ignore
from pysnmp.hlapi.auth import CommunityData  # type: ignore
from pysnmp.smi.rfc1902 import ObjectType  # type: ignore
from pysnmp.smi.error import SmiError  # type: ignore


def rename_key(value: str) -> str:
    """strips some stuff"""
    return value.lstrip("if")


def octets_to_bytes(value: str) -> str | int:
    try:
        return int(value) * 8
    except ValueError:
        return value


async def update_data_bulk(
    config: Config,
    oi: List[Tuple[str,] | Tuple[str, str]],
    data: Dict[str, Any],
    key_alter: Callable[[str], str] = rename_key,
    value_alter: Callable[[str], str | int] = lambda x: x,
) -> None:

    engine = SnmpEngine()

    try:

        async for errorIndication, errorStatus, errorIndex, varBinds in bulkWalkCmd(
            engine,
            CommunityData(config.community),  # defaults to snmpv2c
            UdpTransportTarget(
                transportAddr=(config.hostname, config.port),
                timeout=config.timeout,
                retries=config.retries,
            ),
            ContextData(),
            0,
            config.max_interfaces,
            *oi,
            lexicographicMode=True,
            maxRows=config.max_interfaces,
        ):
            if errorIndication:
                logger.error("errorIndication: {}", errorIndication)
            elif errorStatus:
                logger.error("errorStatus: {}", errorStatus)
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
    except SmiError as error:
        logger.error("SMIERROR: {}", error)
        return


def do_action(config: Config, oi: List[ObjectType]) -> Dict[str, Any]:
    """does the data collection phase"""
    data: Dict[str, Any] = {}

    logger.debug("Running collection...")
    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        update_data_bulk(
            config=config,
            oi=oi,
            data=data,
        )
    )

    # clean up some things
    for value in data.values():
        if "OperStatus" not in value:
            continue
        if "InOctets" in value:
            value["InBytes"] = octets_to_bytes(value["InOctets"])
            del value["InOctets"]
        if "OutOctets" in value:
            value["OutBytes"] = octets_to_bytes(value["OutOctets"])
            del value["OutOctets"]
        print(json.dumps(value))
    return data
