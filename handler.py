import json
import random
import boto3
import uuid

MAX_NUM_WORDS_TO_CONSIDER = 30

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
    new_word = event['body']

    words_table.put_item(
        TableName='fishbowl_words',
        Item={
            'id': str(uuid.uuid1()),
            'word': new_word,
            # todo add in-bowl status
        }
    )
    return {'statusCode': 200, 'body': json.dumps({'message': 'added word: ' + new_word, 'input': event})}


def get_word(event, context):
    # should use scan for this to get a bunch of words then choose 1 randomly
    #   ^ see https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html

    words_response = words_table.scan(
        ProjectionExpression='word',
        Limit=MAX_NUM_WORDS_TO_CONSIDER,
        # todo filter for in-bowl words
    )
    print(str(words_response))
    response_items = words_response['Items']
    if len(response_items) == 0:
        return {'statusCode': 500,
                'error': 'no items in db'}
    random_item = random.choice(response_items)
    print(str(random_item))
    random_word = random_item['word']['S']
    return {"statusCode": 201,
            "body": json.dumps({"message": random_word,
                                "input": event})
            }
