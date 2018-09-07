import boto3
from elasticsearch import Elasticsearch,RequestsHttpConnection
from copy import copy
import json

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

def comment(event,context):
  event = json.loads(event['body'])
  new_comment = copy(event)
  del new_comment['reportId']
  es.update(index='data',doc_type='crime',id=event['reportId'],body={
    'script':{
      'source':'if (!ctx._source.containsKey(\"comments\")) {ctx._source.comments=params.array} else {ctx._source.comments.add(params.item)}',
      'lang':'painless',
      'params':{
        'array':[new_comment],
        'item':new_comment
      }
    }
  })
  es.update(index='data',doc_type='crime',id=event['reportId'],body={
    'script':{
      'source':'if (!ctx._source.containsKey(\"commentCount\")) {ctx._source.commentCount = 1} else {ctx._source.commentCount+=1}',
      'lang':'painless'
    }
  })
  source_doc = es.get(index='data',doc_type='crime',id=event['reportId'])['_source']
  if 'followers' in source_doc:
    for follower in source_doc['followers']:
      lambda_client.invoke(FunctionName='send',Payload=json.dumps({'body':json.dumps({
        'id':follower,
        'body':new_comment['message'],
        'message':source_doc['message'],
        'user':new_comment['userId'],
        '__type__':'comment'
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
    