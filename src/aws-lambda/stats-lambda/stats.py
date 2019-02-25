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
es = connectES('search-hacktps2-xwj2g3yf6o4ybmz4nfj4kcibwu.us-east-2.es.amazonaws.com')

def stats(event,context):
  june_1_2018 = 1527825600000   # includes all organic data, excludes all SFPD data timestamps
  # week_ago = (time.time()-3600*24*365)*1000
  query_dict = {
      'query': {
        'bool': {
          'must': [
            {
            'range': {
              'time': {
                'gte': june_1_2018
              }
            }
            },
            {
            'term': {
              'status':''
            }
            }
          ]
        }
      }
    }
  result = {}
  for term in 'pending','in progress','solved by public','solved by police':
    query_dict['query']['bool']['must'][1]['term']['status'] = term
    result[term] = es.count(index='data',doc_type='crime',body=query_dict)['count']
  result['total'] = sum(result.values())
  return { 
    'isBase64Encoded': True,
    'statusCode': 200,
    'body': json.dumps(result),
    'headers': {
       'Content-Type': 'application/json', 
       'Access-Control-Allow-Origin': '*' 
    }
  }