"""Get the working summary in JIRA."""
from .jira_connector import worklog_dataframe


if __name__ == '__main__':
    worklog_dataframe('2020-05-14')
