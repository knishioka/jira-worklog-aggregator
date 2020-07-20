import pytest
from jira import Issue, Worklog

from worklog_aggregator.jira_connector import worklog_to_dict, extract_issue_worklogs, worklog_logged_issue_keys


def raw_worklog():
    return {
        "self": "https://example.com/rest/api/2/issue/1001/worklog/2001",
        "author": {
            "self": "https://example.com/rest/api/2/user?accountId=012345",
            "accountId": "012345",
            "displayName": "user1",
            "active": True,
            "timeZone": "Asia/Tokyo",
            "accountType": "atlassian",
        },
        "updateAuthor": {
            "self": "https://example.com/rest/api/2/user?accountId=012345",
            "accountId": "012345",
            "displayName": "user1",
            "active": True,
            "timeZone": "Asia/Tokyo",
            "accountType": "atlassian",
        },
        "created": "2020-04-01T17:00:00.000+0900",
        "updated": "2020-04-01T18:00:00.000+0900",
        "started": "2020-04-01T11:00:00.000+0900",
        "timeSpent": "6h",
        "timeSpentSeconds": 21600,
        "id": "2001",
        "issueId": "1001",
    }


@pytest.fixture
def jira_worklog():
    raw = raw_worklog()
    return Worklog(None, None, raw=raw)


@pytest.fixture
def jira_issue():
    raw = {
        "id": "1001",
        "self": "https://bebit-sw.atlassian.net/rest/api/2/issue/1001",
        "key": "KEY-1",
        "fields": {"summary": "This is the summary", "worklog": {"worklogs": [raw_worklog()]}},
    }
    return Issue(None, None, raw=raw)


def test_worklog_logged_issue_keys(jira_issue, mocker):
    issues_mock = mocker.Mock()
    issues_mock.search_issues.return_value = [jira_issue]
    mocker.patch("worklog_aggregator.jira_connector.jira_connection").return_value = issues_mock
    assert worklog_logged_issue_keys("2020-03-01", "2020-03-31") == ["KEY-1"]


def test_extract_issue_worklogs(jira_issue, mocker):
    issue_mock = mocker.Mock()
    issue_mock.issue.return_value = jira_issue
    mocker.patch("worklog_aggregator.jira_connector.jira_connection").return_value = issue_mock
    assert extract_issue_worklogs("2020-01-01")[0]["spent_hours"] == 6.0


def test_worklog_to_dict(jira_worklog):
    expected_dict = {
        "spent_hours": 6.0,
        "created": "2020-04-01",
        "updated": "2020-04-01",
        "started": "2020-04-01",
        "user": "user1",
    }
    assert worklog_to_dict(jira_worklog) == expected_dict
