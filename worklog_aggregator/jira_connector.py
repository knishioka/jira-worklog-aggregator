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


def worklog_dataframe(start_date, end_date):
    """Get worklog dataframe updated on `date`.

    Args:
        start_date(str): start date of worklog range.
        end_date (str): end date of worklog range.

    Returns:
         pandas.DataFrame: worklog dataframe.

    """
    issue_keys = worklog_updated_issue_keys(start_date, end_date)
    date_range = pd.date_range(start_date, end_date).strftime('%Y-%m-%d')
    return pd.concat(
        [pd.DataFrame(d) for d in map(extract_issue_worklogs, issue_keys)]
    ).pipe(lambda df: df[df.updated.isin(date_range)]).reset_index(drop=True)


def worklog_updated_issue_keys(start_date, end_date):
    """Get issues which worklog was updated.

    Args:
        start_date (str): start date of worklog range.
        end_date (str): end date of worklog range.

    Retuns
        list of str: issue key list.

    Examples
        >>> worklog_updated_issue_keys('2020-01-01', '2020-01-31')
        ['KEY-1', 'KEY-2', 'KEY-3']

    """
    issues = jira_connection().search_issues(f"worklogDate >= {start_date} AND  worklogDate <= {end_date}")
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
        'spent_hours': worklog.timeSpentSeconds/60/60,
        'created': parse(worklog.created).date().strftime('%Y-%m-%d'),
        'updated': parse(worklog.updated).date().strftime('%Y-%m-%d'),
        'user': worklog.updateAuthor.displayName
    }
