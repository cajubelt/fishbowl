import json
from random import randint


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
    return {"statusCode": 201, "body": json.dumps({"message": str(randint(1, 50)), "input": event})}
