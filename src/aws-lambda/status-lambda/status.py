import boto3
from elasticsearch import Elasticsearch,RequestsHttpConnection
from copy import copy
import json
import time

def connectES(esEndPoint):
  print ('Connecting to the ES Endpoint {0}'.format(esEndPoint))
  try:
    esClient = Elasticsearch(
    hosts=[{'host': esEndPoint, 'port': 443}],
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection)
    return esClient
  except Exception as E:
    print("Unable to connect to {0}".format(esEndPoint))
    print(E)
    exit(3)
es = connectES('search-hacktps-2xwfbumjkznhuydichzbdudpe4.us-east-2.es.amazonaws.com')
lambda_client = boto3.client('lambda')

def status(event,context):
  event = json.loads(event['body'])
  es.update(index='data',doc_type='crime',id=event['reportId'],body={
    'doc':{
      event['field']:event['value']
    }
  })
  if event['field']=='status':
    if event['value'] in ['solved by public','solved by police']:
      orig_user = es.get(index='data',doc_type='crime',id=event['reportId'])['_source']['reportingUser']
      lambda_client.invoke(FunctionName='token',Payload=json.dumps({'body':json.dumps({
        'userId':orig_user,
        'action':True
      })}))
    lambda_client.invoke(FunctionName='comment',Payload=json.dumps({'body':json.dumps({
      'userId':'San Francisco Police',
      'message':'Thanks for all your collaboration! This report is now %s' % event['value'],
      'reportId':event['reportId'],
      'timestamp':time.time()*1000
    })}))
  return { 
    'isBase64Encoded': True,
    'statusCode': 200,
    'body': '',
    'headers': {
      'Content-Type': 'application/json', 
      'Access-Control-Allow-Origin': '*' 
    }
  }
    