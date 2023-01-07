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
    # return auth URL
    callback_url = "https://master.d2sgt6j88zdzc6.amplifyapp.com/"
    request_endpoint_url = "https://api.twitter.com/oauth/request_token"
    authenticate_url = "https://api.twitter.com/oauth/authenticate"

    session_req = OAuth1Session(API_KEY, API_KEY_SECRET)
    response_req = session_req.post(request_endpoint_url, params={"oauth_callback": callback_url})
    response_req_text = response_req.text

    oauth_token_kvstr = response_req_text.split("&")
    token_dict = {x.split("=")[0]: x.split("=")[1] for x in oauth_token_kvstr}
    oauth_token = token_dict["oauth_token"]

    ret = f"{authenticate_url}?oauth_token={oauth_token}"
    print("認証URL:", ret)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "url": ret,
            # "location": ip.text.replace("\n", "")
        }),
        "headers": {
            "Access-Control-Allow-Origin": "https://master.d2sgt6j88zdzc6.amplifyapp.com",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Methods": "GET,POST",
            "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN",
        }
    }
