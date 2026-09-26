
import pytest

from toolkit.__main__ import main


def test_cli_calc_positive(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["calc", "2+2"])
    out, err = capsys.readouterr()

    assert code == 0
    assert float(out.strip()) == 4
    assert err == ""


def test_cli_calc_negative(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["calc", "1/0"])
    out, err = capsys.readouterr()

    assert code == 2
    assert out == ""
    assert "Ошибка" in err


def test_cli_help(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])

    assert exc_info.value.code == 0
    assert "calc" in capsys.readouterr().out


def test_cli_convert_positive(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["convert", "1", "--from", "cm", "--to", "mm"])
    out, err = capsys.readouterr()

    assert code == 0
    assert out.strip() == "1 cm -> 10 mm"
    assert err == ""


def test_cli_missing_argument(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["convert", "10", "--from", "to"])

    assert exc_info.value.code == 2
    assert "--to" in capsys.readouterr().err

