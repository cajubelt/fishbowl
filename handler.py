import json
import random
import boto3
import uuid

MAX_NUM_WORDS_TO_CONSIDER = 30

dynamodb = boto3.resource('dynamodb', region_name='us-east-1') #, endpoint_url='https://dynamodb.us-east-1.amazonaws.com')
words_table = dynamodb.Table('fishbowl_words')


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


def grab_word_from_bag(event, context):  # todo make empty-body post, include id in response, mutate the status (out of bag and active)
    # should use scan for this to get a bunch of words then choose 1 randomly
    #   ^ see https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html
    try:
        words_response = words_table.scan(
            TableName='fishbowl_words',
            # todo filter for in-bowl words
        )
    except:
        print('bad')
        return {'statusCode': 1000}
    print(str(words_response))
    response_items = words_response['Items']
    if len(response_items) == 0:
        return {'statusCode': 404,
                'message': 'No words left in bag'}
    random_item = random.choice(response_items)
    print(str(random_item))
    random_word = random_item['word']
    return {"statusCode": 201,
            "body": json.dumps({"message": random_word,
                                "input": event})
            }
