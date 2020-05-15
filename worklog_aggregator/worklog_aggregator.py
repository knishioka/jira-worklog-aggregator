"""Get the working summary in JIRA."""
import pandas as pd

from .jira_connector import extract_issue_worklogs, worklog_updated_issue_keys

def worklog_dataframe(date):
    """Get worklog dataframe updated on `date`

    Args:
        date(str): worklog updated date.

    Returns:
         pandas.DataFrame: worklog dataframe.

    """
    issue_keys = worklog_updated_issue_keys(date)
    return pd.concat(
        [pd.DataFrame(d) for d in map(extract_issue_worklogs, issue_keys)]
    ).pipe(lambda df: df[df.updated == date])


if __name__ == '__main__':
    worklog_dataframe('2020-05-14')
