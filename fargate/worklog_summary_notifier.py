"""Notify the summary of worklog."""
import base64
import json
import os

import boto3
import requests


def main():
    """Notify the summary of worklogs."""
    print("Notify the summary of worklogs.")


def slack_notify(msg):
    """Notify message on slack channel.

    Args:
        msg (str): slack message.

    Returns:
        requests.models.Response

    """
    if not msg:
        return
    payload_dic = {
        "text": f"```\n{msg}\n```",
        "username": "Jobcan Lambda Notification",
        "channel": os.environ["SLACK_CHANNEL"],
    }
    client = boto3.client("kms")
    slack_webhook_url = client.decrypt(CiphertextBlob=base64.b64decode(os.getenv("ENCRYPTED_SLACK_WEBHOOK_URL")))[
        "Plaintext"
    ]
    res = requests.post(slack_webhook_url, data=json.dumps(payload_dic))
    if not res.ok:
        print(res.text)
        print(f"slack channel: {os.environ['SLACK_CHANNEL']}")
        res.raise_for_status()
