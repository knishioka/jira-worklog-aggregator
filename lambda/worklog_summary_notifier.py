"""Lambda function to notify the summary of worklog."""

from datetime import datetime, timedelta

from worklog_aggregator.jira_connector import worklog_dataframe
from worklog_aggregator.utils import categorize_date


def worklog_handler(event, context):
    """Notify the summary of worklogs."""
    day = datetime.today()
    start_date = (day - timedelta(weeks=1, days=day.weekday())).strftime('%Y-%m-%d')
    end_date = (day - timedelta(weeks=1, days=day.weekday() - 6)).strftime('%Y-%m-%d')
    print(f'Notify the summary of worklogs between {start_date} and {end_date}.')

    df = worklog_dataframe(start_date, end_date)
    print(df.groupby('user').spent_hours.sum().sort_values(ascending=False))

    top_n = 10
    print(df.groupby(['issue_key', 'summary', 'user']).spent_hours.sum().nlargest(top_n))

    df_with_all_worklog = worklog_dataframe(start_date, end_date, include_out_of_date_range=True).assign(
        date_category=lambda x: x.updated.apply(categorize_date, args=(start_date, end_date))
    )
    long_working_issues = df_with_all_worklog.groupby('issue_key').spent_hours.sum().nlargest(top_n).index
    long_work_df = df_with_all_worklog[df_with_all_worklog.issue_key.isin(long_working_issues)].groupby(
        ['issue_key', 'summary', 'user', 'date_category']
    ).spent_hours.sum().unstack('date_category')
    print(long_work_df)
