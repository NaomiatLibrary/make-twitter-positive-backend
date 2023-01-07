import json
# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import boto3
from botocore.exceptions import ClientError
from requests_oauthlib import OAuth1Session


def get_secret():

    

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    # Your code goes here.
# import requests


def lambda_handler(event, context):
    #fetch twitter-app secret
    secret_name = "make-twitter-positive-secrets"
    region_name = "ap-northeast-1"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e
    secret = json.loads( get_secret_value_response['SecretString'] )
    API_KEY = secret['API_KEY']
    API_KEY_SECRET = secret['API_KEY_SECRET']
    # return informations

    oauth_verifier = event['queryStringParameters']['oauth_verifier']
    oauth_token = event['queryStringParameters']['oauth_token']

    access_endpoint_url = "https://api.twitter.com/oauth/access_token"

    session_acc = OAuth1Session(API_KEY, API_KEY_SECRET, oauth_token, oauth_verifier)
    response_acc = session_acc.post(access_endpoint_url, params={"oauth_token": oauth_token,"oauth_verifier": oauth_verifier})
    response_acc_text = response_acc.text

    access_token_kvstr = response_acc_text.split("&")
    acc_token_dict = {x.split("=")[0]: x.split("=")[1] for x in access_token_kvstr}
    access_token = acc_token_dict["oauth_token"]
    access_token_secret = acc_token_dict["oauth_token_secret"]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "access_token":access_token,
            "access_token_secret":access_token_secret,
            "user_id":acc_token_dict["user_id"],
            "screen_name":acc_token_dict["screen_name"]
        }),
        "headers": {
            "Access-Control-Allow-Origin": "https://master.d2sgt6j88zdzc6.amplifyapp.com",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Methods": "GET,POST",
            "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN",
        }
    }
