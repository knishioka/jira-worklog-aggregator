# jira-worklog-aggregator
Get worklogs on JIRA tickets.

## Quick Start
### Setting Env Variables

Copy .env.sample to .env and fill in the environment values by your favorite editor.

```bash
cp .env.sample .env
vim .env
```

### Build image

```bash
docker build . -t jira-worklog-aggregator
```

### Run Script

```bash
docker run --rm -it --env-file=.env  -v .:/usr/src jira-worklog-aggregator python -m worklog_aggregator.worklog_aggregator
```


### Launch jupyter notebook

```bash
docker run --rm -it --env-file=.env  -v .:/usr/src jira-worklog-aggregator jupyter notebook
```
