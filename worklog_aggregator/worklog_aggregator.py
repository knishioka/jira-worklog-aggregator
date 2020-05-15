"""Get the working summary in JIRA."""
import matplotlib.pyplot as plt

from .jira_connector import worklog_dataframe


def main(date):
    """Create the summary of worklog."""
    df = worklog_dataframe(date)

    plt.figure()
    title = f'Spent hours on tickets on {date}'
    df.groupby('user').spent_hours.sum().sort_values(ascending=False).plot.bar(title=title)
    plt.savefig(f'{date}_worklog_summary.png')


if __name__ == '__main__':
    date = '2020-05-14'
