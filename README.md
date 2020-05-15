# jira-worklog-aggregator
Get worklogs on JIRA tickets.

## Quick Start
### Setting Env Variables

Copy .env.sample to .env and fill in the environment values by your favorite editor.

```bash
cp .env.sample .env
vim .env
```

### Install dependent libraries

You can install libraries by pipenv.

```bash
pipenv install
```

### Run Script

```bash
pipenv run python -m worklog_aggregator.worklog_aggregator --date 2020-05-14
```
