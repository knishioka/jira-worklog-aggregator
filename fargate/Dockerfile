FROM python:3.8.6-slim-buster

WORKDIR /usr/src/jira-worklog-aggregator
COPY worklog_aggregator fargate/requirements.txt fargate/worklog_summary_notifier.py /usr/src/jira-worklog-aggregator/
RUN pip install pip==20.2.3 && \
    pip install -r requirements.txt
RUN useradd app
RUN mkdir -p /home/app && chown -R app:app /home/app
USER app

CMD ["python", "./worklog_summary_notifier.py"]
