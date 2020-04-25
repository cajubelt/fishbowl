import json
import random
from typing import Optional

import boto3
import uuid

MAX_NUM_WORDS_TO_CONSIDER = 30

dynamodb = boto3.resource('dynamodb',
                          region_name='us-east-1')
words_table = dynamodb.Table('fishbowl_words')


def say_hello(event, context):
    return {'statusCode': 200, 'body': json.dumps({'msg': 'hello :)'})}

def add_word(event, context):
    print('event type: ' + str(type(event)))
    print(str(event))
    new_word = event['body']

    words_table.put_item(
        TableName='fishbowl_words',
        Item={
            'id': str(uuid.uuid1()),
            'word': new_word,
            'in_bowl': True,
            'is_active': False
        }
    )
    return {'statusCode': 200, 'body': json.dumps({'message': 'added word: ' + new_word, 'input': event}), "headers": {"Access-Control-Allow-Origin": "*"}}


def put_all_back_in_bowl(event, context):
    out_of_bowl_items = get_words_with_status(in_bowl=False)['Items']
    for item in out_of_bowl_items:
        update_word_status(item['id'], in_bowl=True, is_active=False)
    return {'statusCode': 201,
            "body": json.dumps({"message": str(len(out_of_bowl_items)) + " words put back in bowl." +
                                " out_of_bowl_items: " + str(out_of_bowl_items)})}


def get_words_with_status(in_bowl: bool, is_active: Optional[bool] = None) -> dict:
    filter_expression = "in_bowl = :in"
    expression_attribute_values = {
        ':in': in_bowl
    }
    if is_active is not None:
        filter_expression += " AND is_active = :is_active"
        expression_attribute_values[':is_active'] = is_active
    return words_table.scan(
        TableName='fishbowl_words',
        FilterExpression=filter_expression,
        ExpressionAttributeValues=expression_attribute_values
    )


def grab_word_from_bowl(event, context):
    # error out if another word is is_active
    existing_active_words = get_words_with_status(in_bowl=False, is_active=True)['Items']  # should be singleton
    if len(existing_active_words) > 0:
        return {'statusCode': 500,
                'message': 'Another player has an is_active word! ' +
                           'Please ask the last player to return their word to the bowl,' +
                           ' or report that their team got it.'}

    # choose a word
    words_response = get_words_with_status(in_bowl=True)
    response_items = words_response['Items']
    if len(response_items) == 0:
        return {'statusCode': 404,
                'message': 'No words left in bowl'}
    random_item = random.choice(response_items)
    removed_word = random_item['word']
    print('removing ' + removed_word + ' from bowl')
    removed_word_id = random_item['id']

    # set newly removed word to is_active
    update_word_status(removed_word_id, in_bowl=False, is_active=True)

    # send info about newly removed word to client
    return {"statusCode": 201,
            "body": json.dumps({"word": removed_word,
                                "word_id": removed_word_id}),
            "headers": json.dumps({"Access-Control-Allow-Origin": "*"})
            }


def update_word_status(word_id: str,
                       in_bowl: bool,
                       is_active: bool) -> None:
    words_table.update_item(
        Key={'id': word_id},
        UpdateExpression="set in_bowl = :in, is_active = :is_active",
        ExpressionAttributeValues={
            ':in': in_bowl,
            ':is_active': is_active
        },
    )


# "my team got it!" endpoint
def set_active_word_as_inactive(event, context):
    active_words = get_words_with_status(in_bowl=False, is_active=True)
    for item in active_words['Items']:
        update_word_status(item['id'], in_bowl=False, is_active=False)
    return {"statusCode": 200, "message": "updated these active words to inactive / out of bowl: " + str(active_words)}


# "try another" endpoint
def put_active_word_back_in_bowl(event, context):
    active_words = get_words_with_status(in_bowl=False, is_active=True)
    for item in active_words['Items']:
        update_word_status(item['id'], in_bowl=True, is_active=False)
    return {"statusCode": 200, "message": "updated these active words to inactive / in bowl: " + str(active_words)}

