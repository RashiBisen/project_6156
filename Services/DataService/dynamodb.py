import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb =  boto3.resource('dynamodb')
table_name = 'users'
table = dynamodb.Table(table_name)

def get_primary_key(table_name):
    client = boto3.client('dynamodb')
    response = client.describe_table(
        TableName=table_name)
    keys = response['KeySchema']
    
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
    if uni is not None:
        response = table.query(KeyConditionExpression=Key(key).eq(uni))
        items = response['Items']
    elif:
        response.table.scan()
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


