#had to name this tokens bc apparently linux breaks when python files are named token wtf

import json
import boto3

s3 = boto3.resource('s3')
BUCKET_NAME = 'ourblock'
KEY = 'tokens.json'

def token(event,context):
  event = json.loads(event['body'])
  tokens = json.loads(s3.Object(BUCKET_NAME,KEY).get()['Body'].read().decode('utf-8'))
  if 'action' in event:
    if event['userId'] in tokens:
      tokens[event['userId']]+=1
    else:
      tokens[event['userId']] = 1
    s3.Object(BUCKET_NAME,KEY).put(Body=json.dumps(tokens))
  return { 
        'isBase64Encoded': True,
        'statusCode': 200,
        'body': tokens[event['userId']] if event['userId'] in tokens else 0,
        'headers': {
           'Content-Type': 'application/json', 
           'Access-Control-Allow-Origin': '*' 
       }
  }