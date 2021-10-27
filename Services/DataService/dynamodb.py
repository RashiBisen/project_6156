import boto3
from boto3.dynamodb.conditions import Key, Attr
from dotenv import dotenv_values
from create_dynamodb_table import create_users_table

config = dotenv_values("google_key.env")
aws_access_key_id=config["AWS_Access_Key_ID"]
aws_secret_access_key=config["AWS_Secret_Access_Key"]
region_name=config["region_name"]

dynamodb =  boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key,
                           region_name=region_name, endpoint_url="http://localhost:8000")

client = boto3.client('dynamodb', aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=region_name, endpoint_url="http://localhost:8000")

table_name = 'users'
existing_tables = client.list_tables()['TableNames']
if table_name not in existing_tables:
    create_users_table(dynamodb)
table = dynamodb.Table(table_name)

def get_primary_key(table_name):

    response = client.describe_table(
        TableName=table_name)
    keys = response['Table']['KeySchema']
    
    primary_key =''
    for key in keys:
        if key['KeyType'] == 'HASH':
            primary_key = key['AttributeName']
    return primary_key

def create(uni, data):
    key = get_primary_key(table_name)
    response = table.query(KeyConditionExpression=Key(key).eq(uni))
    items = response['Items']
    if len(items) != 0:
        return False                        # uni already present in DB
    else:
        response = table.put_item(Item=data, ReturnValues='UPDATED_NEW')
        return response

def find_record(uni = None, template = None):
    key = get_primary_key(table_name)
    items = []
    if uni is not None:
        response = table.query(KeyConditionExpression=Key(key).eq(uni))
        items = response['Items']
    else:
        response = table.scan()
        items = response['Items']

    res= []
    if template is not None:
        for record in items:
            flag = 1
            for k, v in template.items():
                if v not in record[k]:
                    flag = 0
                    break
            if flag:
                res.append(record)
    return res

def update_by_key(uni, update_dict):
    key = get_primary_key(table_name)
    response = table.update_item(Key={key: uni},
                AttributeUpdates=update_dict, 
                ReturnValues="UPDATED_NEW")
    return response


