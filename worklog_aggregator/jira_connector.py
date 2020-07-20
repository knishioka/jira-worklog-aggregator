"""Modules to get issues from JIRA."""
import os
from dateutil.parser import parse
from functools import lru_cache

import pandas as pd
from jira import JIRA


@lru_cache(None)
def jira_connection():
    """Create jira connection."""
    options = {"server": os.environ["JIRA_SERVER"]}
    return JIRA(options, basic_auth=(os.environ["JIRA_ID"], os.environ["JIRA_TOKEN"]))


def worklog_dataframe(start_date, end_date, include_out_of_date_range=False):
    """Get worklog dataframe started between `start_date` and `end_date`.

    Args:
        start_date(str): start date of worklog range.
        end_date (str): end date of worklog range.
        include_out_of_date_range (bool): include worklogs out of specified date range.

    Returns:
         pandas.DataFrame: worklog dataframe.

    """
    if start_date > end_date:
        raise ValueError("start_date must be no later than end_date.")
    issue_keys = worklog_started_issue_keys(start_date, end_date)
    date_range = pd.date_range(start_date, end_date).strftime("%Y-%m-%d")
    worklog_df = pd.concat([pd.DataFrame(d) for d in map(extract_issue_worklogs, issue_keys)])
    if include_out_of_date_range:
        return worklog_df.reset_index(drop=True)
    else:
        return worklog_df.pipe(lambda df: df[df.started.isin(date_range)]).reset_index(drop=True)


@lru_cache(None)
def worklog_started_issue_keys(start_date, end_date):
    """Get issues which worklog started time is between start_date and end_date.

    Args:
        start_date (str): start date of worklog range.
        end_date (str): end date of worklog range.

    Retuns
        list of str: issue key list.

    Examples
        >>> worklog_started_issue_keys('2020-01-01', '2020-01-31')
        ['KEY-1', 'KEY-2', 'KEY-3']

    """
    issues = jira_connection().search_issues(
        f"worklogDate >= {start_date} AND  worklogDate <= {end_date}", maxResults=None
    )
    return list(map(lambda x: x.key, issues))


@lru_cache(None)
def extract_issue_worklogs(issue_key):
    """Extract issue worklogs.

    Args:
        issue_key (str): jira issue key.

    """
    issue = jira_connection().issue(issue_key)
    worklogs = map(worklog_to_dict, issue.fields.worklog.worklogs)
    issue_info = {"issue_key": issue.key, "summary": issue.fields.summary}
    worklogs_with_info = [{**wl, **issue_info} for wl in worklogs]
    return list(worklogs_with_info)


def worklog_to_dict(worklog):
    """Create dict from worklog.

    Args:
        worklog (jira.resources.Worklog): jira worklog.

    Returns:
        dict: worklog dict with filtered key.

    """
    return {
        "spent_hours": worklog.timeSpentSeconds / 60 / 60,
        "started": parse(worklog.started).date().strftime("%Y-%m-%d"),
        "created": parse(worklog.created).date().strftime("%Y-%m-%d"),
        "updated": parse(worklog.updated).date().strftime("%Y-%m-%d"),
        "user": worklog.updateAuthor.displayName,
    }
