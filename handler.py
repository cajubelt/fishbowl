import json
from random import random


def hello(event, context):
    body = {
        "message": "Hello Keryn and Chris!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def get_word(event, context):
    return {"statusCode": 200, "body": json.dumps({"message": str(random.randint(5))})}

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
