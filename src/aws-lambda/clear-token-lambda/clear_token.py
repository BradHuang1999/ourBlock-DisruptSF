import json
import boto3

s3 = boto3.resource('s3')
BUCKET_NAME = 'ourblock'
KEY = 'tokens.json'

def clear_token(event,context):
    s3.Object(BUCKET_NAME,KEY).put(Body='{}')
    return { 
        'isBase64Encoded': True,
        'statusCode': 200,
        'body': '',
        'headers': {
           'Content-Type': 'application/json', 
           'Access-Control-Allow-Origin': '*' 
       }
  }