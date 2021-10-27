import boto3


def create_users_table(dyn_resource=None):
    """
    Creates a DynamoDB table.

    :param dyn_resource: Either a Boto3 or DAX resource.
    :return: The newly created table.
    """
    if dyn_resource is None:
        dyn_resource = boto3.resource('dynamodb')

    table_name = 'users'
    params = {
        'TableName': table_name,
        'KeySchema': [
            {'AttributeName': 'uni', 'KeyType': 'HASH'}

        ],
        'AttributeDefinitions': [
            {'AttributeName': 'uni', 'AttributeType': 'S'}

        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    }
    table = dyn_resource.create_table(**params)
    print(f"Creating {table_name}...")
    table.wait_until_exists()
    return table

#
# if __name__ == '__main__':
#     user_table = create_users_table()
#     print(f"Created table.")