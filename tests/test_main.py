"""Test cases for the __main__ module."""
import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

import git_portfolio.__main__
import git_portfolio.response_objects as res


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@pytest.fixture
def mock_config_manager(mocker: MockerFixture) -> MockerFixture:
    """Fixture for mocking CONFIG_MANAGER."""
    mock = mocker.patch("git_portfolio.__main__.CONFIG_MANAGER")
    mock.config_is_empty.return_value = False
    mock.config.github_selected_repos = ["staticdev/omg"]
    return mock


@pytest.fixture
def mock_github_manager(mocker: MockerFixture) -> MockerFixture:
    """Fixture for mocking GithubManager."""
    return mocker.patch("git_portfolio.github_manager.GithubManager", autospec=True)


@pytest.fixture
def mock_config_init_use_case(mocker: MockerFixture) -> MockerFixture:
    """Fixture for mocking ConfigInitUseCase."""
    return mocker.patch(
        "git_portfolio.use_cases.config_init_use_case.ConfigInitUseCase", autospec=True
    )


@pytest.fixture
def mock_config_repos_use_case(mocker: MockerFixture) -> MockerFixture:
    """Fixture for mocking ConfigReposUseCase."""
    return mocker.patch(
        "git_portfolio.use_cases.config_repos_use_case.ConfigReposUseCase",
        autospec=True,
    )


@pytest.fixture
def mock_git_use_case(mocker: MockerFixture) -> MockerFixture:
    """Fixture for mocking GitUseCase."""
    return mocker.patch(
        "git_portfolio.use_cases.git_use_case.GitUseCase", autospec=True
    )


@pytest.fixture
def mock_gh_create_issue_use_case(mocker: MockerFixture) -> MockerFixture:
    """Fixture for mocking GhCreateIssueUseCase."""
    return mocker.patch(
        "git_portfolio.use_cases.gh_create_issue_use_case.GhCreateIssueUseCase",
        autospec=True,
    )


@pytest.fixture
def mock_gh_create_pr_use_case(mocker: MockerFixture) -> MockerFixture:
    """Fixture for mocking GhCreatePrUseCase."""
    return mocker.patch(
        "git_portfolio.use_cases.gh_create_pr_use_case.GhCreatePrUseCase",
        autospec=True,
    )


@pytest.fixture
def mock_gh_merge_pr_use_case(mocker: MockerFixture) -> MockerFixture:
    """Fixture for mocking GhMergePrUseCase."""
    return mocker.patch(
        "git_portfolio.use_cases.gh_merge_pr_use_case.GhMergePrUseCase",
        autospec=True,
    )


@pytest.fixture
def mock_gh_delete_branch_use_case(mocker: MockerFixture) -> MockerFixture:
    """Fixture for mocking GhDeleteBranchUseCase."""
    return mocker.patch(
        "git_portfolio.use_cases.gh_delete_branch_use_case.GhDeleteBranchUseCase",
        autospec=True,
    )


@pytest.fixture
def mock_prompt_inquirer_prompter(mocker: MockerFixture) -> MockerFixture:
    """Fixture for mocking prompt.InquirerPrompter."""
    return mocker.patch("git_portfolio.prompt.InquirerPrompter", autospec=True)


def test_gitp_config_check_success(
    mock_config_manager: MockerFixture, runner: CliRunner
) -> None:
    """It outputs success message."""

    @git_portfolio.__main__.main.command("test")
    @git_portfolio.__main__.gitp_config_check
    def _() -> res.ResponseSuccess:
        return res.ResponseSuccess("success message")

    result = runner.invoke(git_portfolio.__main__.main, ["test"], prog_name="gitp")

    assert "success message" in result.output


def test_gitp_config_check_execute_error(
    mock_config_manager: MockerFixture, runner: CliRunner
) -> None:
    """It calls a command an error response."""

    @git_portfolio.__main__.main.command("test")
    @git_portfolio.__main__.gitp_config_check
    def _() -> res.ResponseFailure:
        return res.ResponseFailure.build_system_error("some error msg")

    result = runner.invoke(git_portfolio.__main__.main, ["test"], prog_name="gitp")

    assert "Error: some error msg" in result.output


def test_gitp_config_check_no_repos(
    mock_config_manager: MockerFixture, runner: CliRunner
) -> None:
    """It outputs no repos selected error message."""

    @git_portfolio.__main__.main.command("test")
    @git_portfolio.__main__.gitp_config_check
    def _() -> res.ResponseFailure:
        return res.ResponseFailure.build_system_error("some error msg")

    mock_config_manager.config_is_empty.return_value = True
    result = runner.invoke(git_portfolio.__main__.main, ["test"], prog_name="gitp")

    assert result.output.startswith("Error: no config found")


def test_add_success(
    mock_git_use_case: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It calls add with '.'."""
    runner.invoke(git_portfolio.__main__.main, ["add", "."], prog_name="gitp")

    mock_git_use_case.return_value.execute.assert_called_once_with(
        ["staticdev/omg"], "add", (".",)
    )


def test_checkout_success(
    mock_git_use_case: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It calls checkout with master."""
    runner.invoke(git_portfolio.__main__.main, ["checkout", "master"], prog_name="gitp")

    mock_git_use_case.return_value.execute.assert_called_once_with(
        ["staticdev/omg"], "checkout", ("master",)
    )


def test_checkout_new_branch(
    mock_git_use_case: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It calls checkout with master."""
    runner.invoke(
        git_portfolio.__main__.main, ["checkout", "-b", "new-branch"], prog_name="gitp"
    )

    mock_git_use_case.return_value.execute.assert_called_once_with(
        ["staticdev/omg"],
        "checkout",
        (
            "-b",
            "new-branch",
        ),
    )


def test_commit_success(
    mock_git_use_case: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It calls commit with message."""
    runner.invoke(
        git_portfolio.__main__.main, ["commit", "-m", "message"], prog_name="gitp"
    )

    mock_git_use_case.return_value.execute.assert_called_once_with(
        ["staticdev/omg"], "commit", ("-m", "message")
    )


def test_pull_success(
    mock_git_use_case: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It calls pull."""
    runner.invoke(git_portfolio.__main__.main, ["pull"], prog_name="gitp")

    mock_git_use_case.return_value.execute.assert_called_once_with(
        ["staticdev/omg"], "pull", ()
    )


def test_push_success(
    mock_git_use_case: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It calls push with origin master."""
    runner.invoke(
        git_portfolio.__main__.main, ["push", "origin", "master"], prog_name="gitp"
    )

    mock_git_use_case.return_value.execute.assert_called_once_with(
        ["staticdev/omg"], "push", ("origin", "master")
    )


def test_push_with_extra_arguments(
    mock_git_use_case: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It calls push with --set-upstream origin new-branch."""
    runner.invoke(
        git_portfolio.__main__.main,
        ["push", "--set-upstream", "origin", "new-branch"],
        prog_name="gitp",
    )

    mock_git_use_case.return_value.execute.assert_called_once_with(
        ["staticdev/omg"], "push", ("--set-upstream", "origin", "new-branch")
    )


def test_reset_success(
    mock_git_use_case: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It calls reset with HEAD^."""
    runner.invoke(git_portfolio.__main__.main, ["reset", "HEAD^"], prog_name="gitp")

    mock_git_use_case.return_value.execute.assert_called_once_with(
        ["staticdev/omg"], "reset", ("HEAD^",)
    )


def test_reset_success_with_hard(
    mock_git_use_case: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It calls reset with --hard HEAD^."""
    runner.invoke(
        git_portfolio.__main__.main, ["reset", "--hard", "HEAD^"], prog_name="gitp"
    )

    mock_git_use_case.return_value.execute.assert_called_once_with(
        ["staticdev/omg"], "reset", ("--hard", "HEAD^")
    )


def test_status_success(
    mock_git_use_case: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It calls status."""
    runner.invoke(git_portfolio.__main__.main, ["status"], prog_name="gitp")

    mock_git_use_case.return_value.execute.assert_called_once_with(
        ["staticdev/omg"], "status", ()
    )


def test_config_init(
    mock_github_manager: MockerFixture,
    mock_config_manager: MockerFixture,
    mock_config_init_use_case: MockerFixture,
    runner: CliRunner,
) -> None:
    """It executes config init use case."""
    config_manager = mock_config_manager.return_value
    github_manager = mock_github_manager.return_value
    mock_config_init_use_case(
        config_manager, github_manager
    ).execute.return_value = res.ResponseSuccess("success message")
    result = runner.invoke(git_portfolio.__main__.configure, ["init"], prog_name="gitp")

    mock_config_init_use_case(
        config_manager, github_manager
    ).execute.assert_called_once()
    assert result.output == "success message\n"


def test_config_repos_success(
    mock_prompt_inquirer_prompter: MockerFixture,
    mock_github_manager: MockerFixture,
    mock_config_manager: MockerFixture,
    mock_config_repos_use_case: MockerFixture,
    runner: CliRunner,
) -> None:
    """It executes config repos use case."""
    config_manager = mock_config_manager.return_value
    mock_config_manager.config_is_empty.return_value = False
    mock_prompt_inquirer_prompter.new_repos.return_value = True
    mock_config_repos_use_case(
        config_manager
    ).execute.return_value = res.ResponseSuccess("success message")
    result = runner.invoke(
        git_portfolio.__main__.configure, ["repos"], prog_name="gitp"
    )

    mock_config_repos_use_case(config_manager).execute.assert_called_once()
    assert result.output == "success message\n"


def test_config_repos_do_not_change(
    mock_prompt_inquirer_prompter: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It does not change config file."""
    mock_config_manager.config_is_empty.return_value = False
    mock_prompt_inquirer_prompter.new_repos.return_value = False
    result = runner.invoke(
        git_portfolio.__main__.configure, ["repos"], prog_name="gitp"
    )

    assert result.exit_code == 0


def test_create_issues(
    mock_gh_create_issue_use_case: MockerFixture,
    mock_github_manager: MockerFixture,
    mock_prompt_inquirer_prompter: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It executes gh_create_issue_use_case."""
    runner.invoke(git_portfolio.__main__.create, ["issues"], prog_name="gitp")
    manager = mock_github_manager.return_value

    mock_gh_create_issue_use_case(manager).execute.assert_called_once()


def test_create_prs(
    mock_gh_create_pr_use_case: MockerFixture,
    mock_github_manager: MockerFixture,
    mock_prompt_inquirer_prompter: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It executes gh_create_pr_use_case."""
    runner.invoke(git_portfolio.__main__.create, ["prs"], prog_name="gitp")
    manager = mock_github_manager.return_value

    mock_gh_create_pr_use_case(manager).execute.assert_called_once()


def test_merge_prs(
    mock_gh_merge_pr_use_case: MockerFixture,
    mock_github_manager: MockerFixture,
    mock_prompt_inquirer_prompter: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It executes gh_merge_pr_use_case."""
    runner.invoke(git_portfolio.__main__.merge, ["prs"], prog_name="gitp")
    manager = mock_github_manager.return_value

    mock_gh_merge_pr_use_case(manager).execute.assert_called_once()


def test_delete_branches(
    mock_gh_delete_branch_use_case: MockerFixture,
    mock_github_manager: MockerFixture,
    mock_prompt_inquirer_prompter: MockerFixture,
    mock_config_manager: MockerFixture,
    runner: CliRunner,
) -> None:
    """It call delete_branches from pm.GithubManager."""
    runner.invoke(git_portfolio.__main__.delete, ["branches"], prog_name="gitp")
    manager = mock_github_manager.return_value

    mock_gh_delete_branch_use_case(manager).execute.assert_called_once()
