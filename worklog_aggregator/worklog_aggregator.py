"""Get the working summary in JIRA."""
import argparse
import json
import os
from datetime import datetime, timedelta
from functools import reduce

import matplotlib.pyplot as plt

from .jira_connector import worklog_dataframe
from .utils import categorize_date

plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["figure.figsize"] = 12, 8
plt.rcParams["font.size"] = 18


def main(start_date, end_date):
    """Create the summary of worklog."""
    df = worklog_dataframe(start_date, end_date)

    if not df.empty:
        plt.figure()
        title = f"Spent hours on tickets between {start_date} and {end_date}"
        df.groupby("user").spent_hours.sum().sort_values(ascending=False).plot.bar(title=title)
        plt.axhline(30, linestyle="dashed", color="red")
        plt.savefig(f"{start_date}-{end_date}_worklog_summary.png")

        top_n = 10
        plt.figure()
        title = f"Top {top_n} taking time tickets between {start_date} and {end_date}"
        df.groupby(["issue_key", "user"]).spent_hours.sum().nlargest(top_n).plot.bar(title=title)
        plt.savefig(f"{start_date}-{end_date}_top{top_n}_taking_time.png")
        plt.figure()
        df_with_all_worklog = worklog_dataframe(start_date, end_date, include_out_of_date_range=True).assign(
            date_category=lambda x: x.started.apply(categorize_date, args=(start_date, end_date))
        )
        long_working_issues = df_with_all_worklog.groupby("issue_key").spent_hours.sum().nlargest(top_n).index
        title = (
            f"Top {top_n} taking time tickets between {start_date} "
            f"and {end_date}\nincludes out of date range worklogs"
        )
        long_work_df = (
            df_with_all_worklog[df_with_all_worklog.issue_key.isin(long_working_issues)]
            .groupby(["issue_key", "user", "date_category"])
            .spent_hours.sum()
            .unstack("date_category")
        )
        long_work_df.loc[long_work_df.sum(1).sort_values(ascending=False).index].plot.bar(title=title, stacked=True)
        plt.savefig(f"{start_date}-{end_date}_top{top_n}_taking_time_with_out_of_date_range_work.png")

        if os.getenv("USER_GROUP"):
            user_group = json.loads(os.getenv("USER_GROUP"))
            for group, users in user_group.items():
                group_df = df[df.user.isin(users)]
                title = f"{group} spent hours on tickets between {start_date} and {end_date}"
                plt.figure()
                group_df.groupby("user").spent_hours.sum().sort_values(ascending=False).plot.bar(title=title)
                plt.savefig(f"{start_date}-{end_date}_{group}_worklog_summary.png")
            users_in_config = reduce(lambda x, y: x | set(y), user_group.values(), set())
            missing_users = set(df_with_all_worklog.user) - users_in_config
            if len(missing_users) > 0:
                print(f"No config for {', '.join(missing_users)}")
    else:
        print(f"No worklogs between {start_date} and {end_date}.")


if __name__ == "__main__":
    day = datetime.today()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start_date",
        help="target start date of worklog",
        default=(day - timedelta(weeks=1, days=day.weekday())).strftime("%Y-%m-%d"),
    )
    parser.add_argument(
        "--end_date",
        help="target end date of worklog",
        default=(day - timedelta(weeks=1, days=day.weekday() - 6)).strftime("%Y-%m-%d"),
    )
    args = parser.parse_args()

    main(args.start_date, args.end_date)
