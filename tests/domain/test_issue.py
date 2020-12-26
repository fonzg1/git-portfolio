"""Test cases for the Github issue model."""
import git_portfolio.domain.issue as i


def test_issue_model_init() -> None:
    """Verify model initialization."""
    number = 1
    title = "issue title"
    body = "body description"
    labels = {"testing"}
    test_issue = i.Issue(number, title, body, labels)

    assert test_issue.number == number
    assert test_issue.title == title
    assert test_issue.body == body
    assert test_issue.labels == labels
