# snmp-json

Currently designed to pull interface stats from my router, can be configured to add a bunch of other options.

Only uses SNMPv2c because I'm lazy and it's hard enough to make this junk work 😃

## Config

Env vars:

| Variable | Thing | Example Value (and default) |
| --- | --- | --- |
| `SNMP_JSON_HOSTNAME` | Hostname or IP address of target device | `localhost` |
| `SNMP_JSON_PORT` | UDP port of target device | `161` |
| `SNMP_JSON_COMMUNITY` | SNMPv1 Community to contact | `public` |
| `SNMP_JSON_MAX_INTERFACES` | Maximum number of interfaces to attempt | `32` |
| `SNMP_JSON_INTERVAL` | If set, the interval between starting checks | Unset |
| `SNMP_JSON_DEBUG` | Enable additional debug logging | `False` |
| `SNMP_TIMEOUT` | Number of seconds to wait for an SNMP command | `5` |
