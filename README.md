# jira-worklog-aggregator
Get worklogs on JIRA tickets.

- ![Register jira-worklog-summary-notifier task definition](https://github.com/knishioka/jira-worklog-aggregator/workflows/Register%20jira-worklog-summary-notifier%20task%20definition/badge.svg)
- ![Create jira-worklog-summary-notifier image](https://github.com/knishioka/jira-worklog-aggregator/workflows/Create%20jira-worklog-summary-notifier%20image/badge.svg)
- ![Deploy worklog summary notifier lambda](https://github.com/knishioka/jira-worklog-aggregator/workflows/Deploy%20worklog%20summary%20notifier%20lambda/badge.svg)
- ![Check python code](https://github.com/knishioka/jira-worklog-aggregator/workflows/Check%20python%20code/badge.svg)

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
docker run --rm -p 8888:8888 -it --env-file=.env  -v $(pwd):/usr/src jira-worklog-aggregator jupyter notebook
```

## Lambda Layer
### Create and Publish Lambda Layer

```bash
docker build . -t lambda-layer
docker run --rm -v $(pwd):/dist lambda-layer pandas
aws lambda publish-layer-version --layer-name pandas --zip-file fileb://layer.zip --compatible-runtimes python3.8
docker run --rm -v $(pwd):/dist lambda-layer matplotlib
aws lambda publish-layer-version --layer-name matplotlib --zip-file fileb://layer.zip --compatible-runtimes python3.8
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

# Run on AWS Fargate
## Create Image for worklog-summary-notifier
### Build Image
```bash
docker build . -t ${CONTAINER_REGISTRY_PATH}/jira-worklog-summary-notifier -f fargate/Dockerfile
```

### Create ECR Repository
```bash
aws ecr create-repository --repository-name jira-worklog-summary-notifier
```

### Push image

```bash
docker push ${CONTAINER_REGISTRY_PATH}/jira-worklog-summary-notifier
```

## Set Up Fargate

```bash
aws ecs create-cluster --cluster-name fargate-cluster
```

You need to create a role for `Elastic Container Service Task`.
```bash
sed -i \
    -e "s#EXECUTION_ROLE_ARN#${EXECUTION_ROLE_ARN}#" \
    -e "s#CONTAINER_REPOSITORY_PATH#${EXECUTION_ROLE_ARN}#" \
    -e "s#IMAGE_NAME#${IMAGE_NAME}#" \
    fargate/task_definition.json
aws ecs register-task-definition --cli-input-json file://fargate/task_definition.json
```

```bash
aws ecs create-service \
  --cluster fargate-cluster \
  --service-name fargate-service \
  --task-definition "${FARGATE_TASK_DEFINITION}" \
  --desired-count 1 \
  --launch-type "FARGATE" \
  --network-configuration "awsvpcConfiguration={subnets=[${FARGATE_SUBNET}],securityGroups=[
${FARGATE_SECURITY_GROUP}]}"
```
