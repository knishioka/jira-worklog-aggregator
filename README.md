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
docker run --rm -it --env-file=.env  -v $(pwd):/usr/src jira-worklog-aggregator python -m worklog_aggregator.worklog_aggregator
```


### Launch jupyter notebook

```bash
docker run --rm -it --env-file=.env  -v $(pwd):/usr/src jira-worklog-aggregator jupyter notebook
```

## Lambda Layer
### Create Lambda Layer

```bash
docker build . -t lambda-layer
docker run --rm -v $(pwd):/dist lambda-layer pandas
```

### Publish lambda layer

```bash
aws lambda publish-layer-version --layer-name pandas --zip-file fileb://layer.zip --compatible-runtimes python3.8
```


## Create Lambda Function

```bash
aws lambda create-function \
    --function-name <your function name> \
    --runtime python3.8 \
    --role <your role> \
    --handler worklog_summary_notifier.worklog_handler \
    --zip-file fileb://function.zip
```
