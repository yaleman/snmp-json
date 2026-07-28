""" Test nothing. """

from click.testing import CliRunner

from snmp_json.__main__ import cli


def test_help() -> None:
    """testing the help function"""
    runner = CliRunner()

    result = runner.invoke(cli, "--help")
    assert result.exit_code == 0
