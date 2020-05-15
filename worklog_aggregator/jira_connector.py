"""Modules to get issues from JIRA."""
import os
from dateutil.parser import parse
from functools import lru_cache

import pandas as pd
from jira import JIRA


@lru_cache(None)
def jira_connection():
    """Create jira connection."""
    options = {'server': os.environ['JIRA_SERVER']}
    return JIRA(options, basic_auth=(os.environ['JIRA_ID'], os.environ['JIRA_TOKEN']))


def worklog_dataframe(date):
    """Get worklog dataframe updated on `date`.

    Args:
        date(str): worklog updated date.

    Returns:
         pandas.DataFrame: worklog dataframe.

    """
    issue_keys = worklog_updated_issue_keys(date)
    return pd.concat(
        [pd.DataFrame(d) for d in map(extract_issue_worklogs, issue_keys)]
    ).pipe(lambda df: df[df.updated == date])


def worklog_updated_issue_keys(date):
    """Get issues which worklog was updated.

    Args:
        date (str): worklog updated date.

    Retuns
        list of str: issue key list.

    Examples
        >>> worklog_updated_issue_keys('2020-01-01')
        ['KEY-1', 'KEY-2', 'KEY-3']

    """
    issues = jira_connection().search_issues(f'worklogDate = {date}')
    return list(map(lambda x: x.key, issues))


def extract_issue_worklogs(issue_key):
    """Extract issue worklogs.

    Args:
        issue_key (str): jira issue key.

    """
    issue = jira_connection().issue(issue_key)
    return list(map(worklog_to_dict, issue.fields.worklog.worklogs))


def worklog_to_dict(worklog):
    """Create dict from worklog.

    Args:
        worklog (jira.resources.Worklog): jira worklog.

    Returns:
        dict: worklog dict with filtered key.

    """
    return {
        'spent_seconds': worklog.timeSpentSeconds,
        'created': parse(worklog.created).date().strftime('%Y-%m-%d'),
        'updated': parse(worklog.updated).date().strftime('%Y-%m-%d'),
        'user': worklog.updateAuthor.displayName
    }
