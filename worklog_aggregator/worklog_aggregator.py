"""Get the working summary in JIRA."""
import argparse

import matplotlib.pyplot as plt

from .jira_connector import worklog_dataframe

plt.rcParams['savefig.bbox'] = 'tight'


def main(date):
    """Create the summary of worklog."""
    df = worklog_dataframe(date)

    plt.figure()
    title = f'Spent hours on tickets on {date}'
    df.groupby('user').spent_hours.sum().sort_values(ascending=False).plot.bar(title=title)
    plt.savefig(f'{date}_worklog_summary.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', help='target date of worklog')
    args = parser.parse_args()
    main(args.date)
