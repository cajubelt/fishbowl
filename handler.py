import json
from random import randint
import boto3
import uuid

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
    print('event type: ' + str(type(event)))
    print(str(event))
    new_word = json.loads(event)['body']

    words_table.put_item(
        Item={
            'id': uuid.uuid1(),
            'word': new_word
        }
    )
    return {'statusCode': 200, 'body': json.dumps({'message': 'added word: ' + new_word, 'input': event})}


def get_word(event, context):
    # should use scan for this to get a bunch of words then choose 1 randomly
    #   ^ see https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html
    return {"statusCode": 201, "body": json.dumps({"message": str(randint(1, 50)), "input": event})}
