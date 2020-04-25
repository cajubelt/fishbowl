import json
import random
import boto3
import uuid

MAX_NUM_WORDS_TO_CONSIDER = 30

dynamodb = boto3.resource('dynamodb',
                          region_name='us-east-1')
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
            'in_bowl': True,
            'is_active': False
        }
    )
    return {'statusCode': 200, 'body': json.dumps({'message': 'added word: ' + new_word, 'input': event})}


def grab_word_from_bowl(event,
                        context):
    # should use scan for this to get a bunch of words then choose 1 randomly
    #   ^ see https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html
    words_response = words_table.scan(
        TableName='fishbowl_words',
        FilterExpression="in_bowl = :in",
        ExpressionAttributeValues={
            ':in': True
        }
    )
    response_items = words_response['Items']
    if len(response_items) == 0:
        return {'statusCode': 404,
                'message': 'No words left in bowl'}
    random_item = random.choice(response_items)
    removed_word = random_item['word']
    print('removing ' + removed_word + ' from bowl')
    word_id = random_item['id']
    set_word_as_out_of_bowl_and_active(word_id)
    return {"statusCode": 201,
            "body": json.dumps({"word": removed_word,
                                "word_id": word_id})
            }


def set_word_as_out_of_bowl_and_active(word_id: str) -> None:
    words_table.update_item(
        Key={'id': word_id},
        UpdateExpression="set in_bowl = :in, active = :active",
        ExpressionAttributeValues={
            ':in': False,
            ':active': True
        },
    )
