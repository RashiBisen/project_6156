import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb =  boto3.resource('dynamodb')
table = dynamodb.Table('users')

def get_all_users():
    response = table.query()
    items = response['Items']
    return items

def get_user(uni):
    response = table.query(KeyConditionExpression=Key('uni').eq(uni))
    items = response['Items']
    return items

def update_user(uni, update_dict):
        table.update_item(Key={'uni': uni},
                AttributeUpdates=update_dict)
