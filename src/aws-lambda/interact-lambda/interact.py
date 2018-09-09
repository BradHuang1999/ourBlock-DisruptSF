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

def interact(event,context):
  event = json.loads(event['body'])
  user = event['userId']
  field = event['action']+('' if event['action'].endswith('e') else 'e')+'rs'
  count_field = event['action']+('' if event['action'].endswith('e') else 'e')+'rCount'
  es.update(index='data',doc_type='crime',id=event['reportId'],body={
    'script':{
      'source':'if (!ctx._source.containsKey(\"%s\")) {ctx._source.%s=params.array} else {ctx._source.%s.add(params.item)}' % (field,field,field),
      'lang':'painless',
      'params':{
        'array':[user],
        'item':user
      }
    }
  })
  es.update(index='data',doc_type='crime',id=event['reportId'],body={
    'script':{
      'source':'if (!ctx._source.containsKey(\"%s\")) {ctx._source.%s = 1} else {ctx._source.%s+=1}' % (count_field,count_field,count_field),
      'lang':'painless'
    }
  })
  return { 
    'isBase64Encoded': True,
    'statusCode': 200,
    'body': '',
    'headers': {
      'Content-Type': 'application/json', 
      'Access-Control-Allow-Origin': '*' 
    }
  }
    