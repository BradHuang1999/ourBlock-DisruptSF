import boto3
from elasticsearch import Elasticsearch,RequestsHttpConnection
import json
#from run_prediction import classify
import requests
#from eth_block import sendCrime

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

def post(event,context):
  event = json.loads(event['body'])
  event['status'] = 'pending'
  event['followers'] = [event['reportingUser']]
  defaults = {
    'lat': 0,
    'lon': 0,
    'time': 0,
    'privacy': "public",
    'reportingUser': "system",
    'anonymous': False,
    'message': "",
    'category': "other",
    'upvoters': [],
    'downvoters': [],
    'comments': [],
    'upvoterCount': 0,
    'downvoterCount': 0,
    'followerCount': 1,
    'commentCount': 0
  }
  for key in defaults:
    if key not in event:
      event[key] = defaults[key]
  doc_id = es.index(index='data',doc_type='crime',body=event)['_id']
  output = {'_id':doc_id,'category':event['category']}
  return { 
    'isBase64Encoded': True,
    'statusCode': 200,
    'body': json.dumps(output),
    'headers': {
       'Content-Type': 'application/json', 
       'Access-Control-Allow-Origin': '*' 
   }
  }
