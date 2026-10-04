import pytest

from toolkit.__main__ import main


def test_cli_calc_success(capsys):
    exit_code = main(['calc', '2 + 3 * 4'])
    output = capsys.readouterr()
    assert exit_code == 0
    assert output.out.strip() == '14.0'


def test_cli_error_goes_to_stderr_with_code_2(capsys):
    exit_code = main(['calc', '1 / 0'])
    output = capsys.readouterr()
    assert exit_code == 2
    assert output.out == ''
    assert output.err.strip() != ''


def test_cli_help_exits_with_code_0():
    with pytest.raises(SystemExit) as exit_info:
        main(['--help'])
    assert exit_info.value.code == 0