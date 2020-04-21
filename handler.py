import json
from random import randint
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
words_table = dynamodb.Table('fishbowl-test-words_table')


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


def add_word(event, context):
    new_word = json.loads(event['body'])

    words_table.put_item(
        Item={
            'word': new_word
        }
    )
    return {'statusCode': 200, 'body': json.dumps({'message': 'added word: ' + new_word, 'input': event})}


def get_word(event, context):
    return {"statusCode": 201, "body": json.dumps({"message": str(randint(1, 50)), "input": event})}
