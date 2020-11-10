"""Test cases for the git use case."""
from typing import Any

import pytest
from pytest_mock import MockerFixture

from git_portfolio.use_cases import git_use_case as guc


@pytest.fixture
def mock_popen(mocker: MockerFixture) -> Any:
    """Fixture for mocking subprocess.Popen."""
    mock = mocker.patch("subprocess.Popen")
    mock.return_value.returncode = 0
    mock.return_value.communicate.return_value = (b"some output", b"")
    return mock


def test_check_git_install_success(mock_popen: MockerFixture) -> None:
    """It returns success."""
    response = guc.GitUseCase.check_git_install()

    assert "" == response


def test_check_git_install_error(mock_popen: MockerFixture) -> None:
    """It returns failure with git not installed message."""
    mock_popen.side_effect = FileNotFoundError
    response = guc.GitUseCase.check_git_install()

    assert (
        "This command requires Git executable installed and on system path." == response
    )


def test_execute_success(mock_popen: MockerFixture) -> None:
    """It returns success messages."""
    response = guc.GitUseCase().execute(
        ["staticdev/omg", "staticdev/omg2"], "checkout", ("xx",)
    )

    assert bool(response) is True
    assert response.value == "omg: checkout successful.\nomg2: checkout successful.\n"


def test_execute_success_no_output(mock_popen: MockerFixture) -> None:
    """It returns success message."""
    response = guc.GitUseCase().execute(
        ["staticdev/omg", "staticdev/omg2"], "add", (".",)
    )

    assert bool(response) is True
    assert response.value == "omg: add successful.\nomg2: add successful.\n"


def test_execute_git_not_installed(mock_popen: MockerFixture) -> None:
    """It returns failure with git not installed message."""
    mock_popen.side_effect = FileNotFoundError
    response = guc.GitUseCase().execute(["staticdev/notcloned"], "checkout", ("xx",))

    assert bool(response) is False
    assert (
        "This command requires Git executable installed and on system path."
        == response.value["message"]
    )


def test_execute_no_folder(mocker: MockerFixture, mock_popen: MockerFixture) -> None:
    """It returns that file does not exist."""
    mock_popen.side_effect = [
        mocker.Mock(),
        FileNotFoundError("No such file or directory"),
    ]
    response = guc.GitUseCase().execute(["staticdev/notcloned"], "checkout", ("xx",))

    assert bool(response) is True
    assert response.value == "notcloned: No such file or directory\n"


def test_execute_error_during_execution(mock_popen: MockerFixture) -> None:
    """It returns success message with the error on output."""
    mock_popen.return_value.returncode = 1
    mock_popen().communicate.return_value = (
        b"",
        b"error: pathspec 'xyz' did not match any file(s) known to git",
    )
    response = guc.GitUseCase().execute(["staticdev/notcloned"], "checkout", ("xyz",))

    assert bool(response) is True
    assert (
        response.value
        == "notcloned: error: pathspec 'xyz' did not match any file(s) known to git"
    )
