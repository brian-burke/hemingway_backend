import json
from types import SimpleNamespace

from boto3 import resource, client
import config
from models import User, Profile, Settings

AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
REGION_NAME = config.REGION_NAME
# These 3 are optional, allows use of local dynamodb
DYNAMO_ENABLE_LOCAL = config.DYNAMO_ENABLE_LOCAL
DYNAMO_LOCAL_HOST = config.DYNAMO_LOCAL_HOST
DYNAMO_LOCAL_PORT = config.DYNAMO_LOCAL_PORT

client = client(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)

resource = resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)


# Create initial user table
def create_table(name):
    client.create_table(
        AttributeDefinitions=[  # Name and type of required attributes -> N for Number, B for Binary, S for String
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        TableName=name,  # Table Name
        KeySchema=[  # Primary Key
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        # Provisioned Throughput must be formatted as a dict with the values being integers
        # Otherwise this can be set to Billing Mode - Pay Per Request
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )


user_table = resource.Table('Users')


# profile_table = resource.Table('Profiles')
# settings_table = resource.Table('Settings')
# attributes_table = resource.Table('Attributes')


# add a user to the table
def add_user(user: User):
    user_table.put_item(
        Item={
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'email': user.email,
            'company_name': user.company_name,
            'profiles': user.profiles,
            'settings': user.settings.toJSON()
        }
    )


# def add_settings(user: User):
#     settings_table.put_item(
#         Item={
#             'id': user.id,
#             'phone_number_visibility': user.settings.phone_number_visibility,
#             'company_name_visibility': user.settings.company_name_visibility,
#             'directory_visibility': user.settings.directory_visibility
#         }
#
#     )


# def add_profile(user: User, profile: Profile):
#     profile_table.put_item(
#         Item={
#             'id': user.id + '_' + profile.name,
#             'name': profile.name,
#             'user_id': user.id,
#         }
#
#     )


# read a user from the table by id
def get_item_from_user(id):
    data = user_table.get_item(
        Key={
            'id': id
        },
        AttributesToGet=[
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'company_name',
            'profiles',
            'settings'
        ]
    )
    print('data', data)

    response = data['Item']
    print('response', response)

    settingsJson = json.loads(response['settings'], object_hook=lambda d: SimpleNamespace(**d))

    print('settings json', settingsJson)

    settings = Settings(settingsJson.id, settingsJson.phone_number_visibility, settingsJson.company_name_visibility,
                        settingsJson.directory_visibility)

    return User(response['id'], response['first_name'], response['last_name'], response['phone_number'],
                response['email'], response['company_name'], response['profiles'], settings)


def get_all_users():
    response = user_table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = user_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return data
