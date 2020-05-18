"""Get the working summary in JIRA."""
import argparse

import matplotlib.pyplot as plt

from .jira_connector import worklog_dataframe

plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['figure.figsize'] = 12, 8
plt.rcParams['font.size'] = 18


def main(start_date, end_date):
    """Create the summary of worklog."""
    df = worklog_dataframe(start_date, end_date)

    if not df.empty:
        plt.figure()
        title = f'Spent hours on tickets between {start_date} and {end_date}'
        df.groupby('user').spent_hours.sum().sort_values(ascending=False).plot.bar(title=title)
        plt.savefig(f'{start_date}-{end_date}_worklog_summary.png')

        plt.figure()
        title = f'Top 10 taking time tickets between {start_date} and {end_date}'
        df.groupby(['issue_key', 'user']).spent_hours.sum().nlargest(10).plot.bar()
        plt.savefig(f'{start_date}-{end_date}_top10_taking_time.png')
    else:
        print(f'No worklogs between {start_date} and {end_date}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_date', help='target start date of worklog')
    parser.add_argument('--end_date', help='target end date of worklog')
    args = parser.parse_args()
    main(args.start_date, args.end_date)
