import boto3
from elasticsearch import Elasticsearch,RequestsHttpConnection
from elasticsearch.client import IndicesClient
from elasticsearch.helpers import bulk
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
es = connectES('search-hacktps2-xwj2g3yf6o4ybmz4nfj4kcibwu.us-east-2.es.amazonaws.com')
ind = IndicesClient(es)

def bulk_upload(event,context):
  try:
    ind.delete('data')
  except:
    'Did not find index "data", creating new index.'
  ind.create('data',body={
    'mappings':{
      'crime':{
        'properties':{
          'anonymous':{'type':'boolean'},
          'category':{'type':'keyword'},
          'commentCount':{'type':'long'},
          'comments':{
            'type':'nested',
            'properties':{
              'anonymous':{'type':'boolean'},
              'message':{'type':'text'},
              'timestamp':{'type':'long'},
              'user':{'type':'keyword'},
              'userId':{'type':'keyword'}
            }
          },
          'downvoterCount':{'type':'long'},
          'downvoters':{'type':'keyword'},
          'followerCount':{'type':'long'},
          'followers':{'type':'keyword'},
          'lat':{'type':'float'},
          'lon':{'type':'float'},
          'message':{'type':'text'},
          'privacy':{'type':'keyword'},
          'reportingUser':{'type':'keyword'},
          'status':{'type':'keyword'},
          'time':{'type':'long'},
          'upvoterCount':{'type':'long'},
          'upvoters':{'type':'keyword'}
        }
      }
    }
  })
  data = json.loads(open('Cleaned-Data.json').read())
  bulk(es,[{'_index':'data','_type':'crime','_op_type':'index','_source':item} for item in data])
  return { 
        'isBase64Encoded': True,
        'statusCode': 200,
        'body': '',
        'headers': {
           'Content-Type': 'application/json', 
           'Access-Control-Allow-Origin': '*' 
       }
       }
