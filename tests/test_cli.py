from solodeveling_protocol.cli import main


def test_cli_returns_zero_for_valid_project(capsys) -> None:
    exit_code = main(["tests/fixtures/valid-project"])

    assert exit_code == 0
    assert "Protocol validation passed" in capsys.readouterr().out


def test_cli_returns_one_and_prints_issues_for_invalid_project(capsys) -> None:
    exit_code = main(["tests/fixtures/invalid-done-project"])

    assert exit_code == 1
    assert "done-without-evidence" in capsys.readouterr().out