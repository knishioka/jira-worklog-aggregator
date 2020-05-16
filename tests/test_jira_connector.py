import pytest
from jira import Worklog

from worklog_aggregator.jira_connector import worklog_to_dict


@pytest.fixture
def jira_ticket():
    raw = {'self': 'https://example.com/rest/api/2/issue/1001/worklog/2001',
           'author': {'self': 'https://example.com/rest/api/2/user?accountId=012345',
                      'accountId': '012345',
                      'avatarUrls': {
                          '48x48': '?size=48&s=48',
                          '24x24': 'https://example.com/avatar?size=24&s=24',
                          '16x16': 'https://example.com/avatar?size=16&s=16',
                          '32x32': 'https://example.com/avatar?size=32&s=32'},
                      'displayName': 'user1',
                      'active': True,
                      'timeZone': 'Asia/Tokyo',
                      'accountType': 'atlassian'},
           'updateAuthor': {'self': 'https://example.com/rest/api/2/user?accountId=012345',
                            'accountId': '012345',
                            'avatarUrls': {
                                '48x48': 'https://example.com/avatar?size=48&s=48',
                                '24x24': 'https://example.com/avatar?size=24&s=24',
                                '16x16': 'https://example.com/avatar?size=16&s=16',
                                '32x32': 'https://example.com/avatar?size=32&s=32'},
                            'displayName': 'user1',
                            'active': True,
                            'timeZone': 'Asia/Tokyo',
                            'accountType': 'atlassian'},
           'created': '2020-04-01T17:00:00.000+0900',
           'updated': '2020-04-01T18:00:00.000+0900',
           'started': '2020-04-01T11:00:00.000+0900',
           'timeSpent': '6h',
           'timeSpentSeconds': 21600,
           'id': '2001',
           'issueId': '1001'
           }
    return Worklog(None, None, raw=raw)


def test_worklog_to_dict(jira_ticket):
    expected_dict = {
        'spent_hours': 6.0,
        'created': '2020-04-01',
        'updated': '2020-04-01',
        'user': 'user1'
    }
    assert worklog_to_dict(jira_ticket) == expected_dict
