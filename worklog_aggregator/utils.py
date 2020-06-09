"""Utils for jira worklog aggregator."""


def categorize_date(date, start_date, end_date):
    """Categorize date."""
    if date < start_date:
        return f'< {start_date}'
    elif date > end_date:
        return f'> {end_date}'
    else:
        return f'{start_date} ~ {end_date}'
