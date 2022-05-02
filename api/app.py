from flask import Flask, jsonify, request
from flask_cognito import CognitoAuth, cognito_auth_required, current_user, current_cognito_jwt
from models import User, Profile, Settings
import json
from types import SimpleNamespace
import controller
import jsonpickle

app = Flask(__name__)

app.config.update({
    'COGNITO_REGION': 'us-east-1',
    'COGNITO_USERPOOL_ID': 'us-east-1_uwvkdzxkz',

    # optional
    'COGNITO_APP_CLIENT_ID': 'aiugb6dtchl0mu1ik76pkdtkk',  # client ID you wish to verify user is authenticated against
    'COGNITO_CHECK_TOKEN_EXPIRATION': False,  # disable token expiration checking for testing purposes
    'COGNITO_JWT_HEADER_NAME': 'X-Hemmingway-Authorization',
    'COGNITO_JWT_HEADER_PREFIX': 'Bearer',
})

# initialize extension

cogauth = CognitoAuth(app)


@cogauth.identity_handler
def lookup_cognito_user(payload):
    """Look up user in our database from Cognito JWT payload."""
    return payload['email']


@app.route("/")
def api_private():
    # user must have valid cognito access or ID token in header
    # (accessToken is recommended - not as much personal information contained inside as with idToken)
    # controller.create_table("Users")
    # controller.create_table("Profiles")
    # controller.create_table("Settings")
    # controller.create_table("Attributes")

    return jsonify({
        'name': current_cognito_jwt['name'],  # from cognito pool
        'email': current_cognito_jwt['email'],  # from cognito pool
        'cognito:username': current_cognito_jwt['cognito:username'],  # from cognito pool
    })


@app.route("/user/create", methods=['POST'])
@cognito_auth_required
def create_user():
    payload = json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d))

    settings = Settings(0, False, False, False)
    user = User(payload.id, payload.first_name, payload.last_name, payload.phone_number, payload.email,
                payload.company_name, [], settings)
    controller.add_user(user)
    return user.toJSON()


@app.route("/profile/add", methods=['POST'])
@cognito_auth_required
def add_profile():
    payload = json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d))
    user_id = current_cognito_jwt['cognito:username']
    user = controller.get_item_from_user(user_id)
    profile = Profile(0, payload.name, payload.attributes)
    user.profiles.append(profile)
    controller.add_user(user)


@app.route("/user/<user_id>", methods=['GET'])
@cognito_auth_required
def find_user(user_id):
    print("userID", user_id)

    response = controller.get_item_from_user(user_id)

    return jsonpickle.encode(response, unpicklable=False)


# @app.route("/user", methods=['DELETE'])
# @cognito_auth_required
# def delete_user(id):


# @app.route("/user", methods=['PUT'])
# @cognito_auth_required
# def update_user(id):


@app.route("/user/profile")
@cognito_auth_required
def user_profile():
    liquor = Profile(0, 'liquor', [('whiskey', 'jack daniels'), ('vodka', 'titos')])
    cigar = Profile(0, 'cigar', [('romeo y julieta', 'robusto'), ('cigar2', 'slim')])
    settings = Settings(0, False, False, False)
    user = User(0, 'John', 'Doe', 1234567890, current_cognito_jwt['email'], 'Build Labs', [liquor, cigar], settings)
    return user.toJSON()
