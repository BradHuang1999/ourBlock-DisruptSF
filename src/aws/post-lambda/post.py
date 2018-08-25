import boto3
from elasticsearch import Elasticsearch,RequestsHttpConnection
import json
#from run_prediction import classify
import requests
#from eth_block import sendCrime

def post(event,context):
  event = json.loads(event['body'])
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
  es.index(index='data',doc_type='crime',body=event['body'])
  try:
    query_dict = {
      'query': {
        'bool': {
          'must': {
            'term': {
              'Year':event['body']['Year']
            },
            'term': {
              'Month':event['body']['Month']
            },
            'range': {
              'Day': {
                'gte':event['body']['day']-3,
                'lte':event['body']['day']
              }
            },
            'range': {
              'Latitude': {
                'gte':event['body']['Latitude']-0.0005,
                'lte':event['body']['Latitude']+0.0005
              }
            },
            'range': {
              'Longitude': {
                'gte':event['body']['Longitude']-0.0005,
                'lte':event['body']['Longitude']+0.0005
              }
            },
            'term': {
              'Class':event['body']['Class']
            }
          }
        }
      }
    }
    num_results = es.search(index='data',doc_type='crime',size=0,body=query_dict)['hits']['total']
  except:
    num_results = 0
  if 'Class' not in event['body'] or event['body']['Class'] in ['Assault','Homicide','Sexual Assault'] or (event['body']['Confidence']>0.5 and num_results>1):
    requests.post('https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/send',data={'id':'_all','body':'Crime reported: '+event['body']['Description'] if 'Description' in event['body'] else 'no description.'})
  #sendCrime(event['body']['Latitude'],event['body']['Longitude'],event['body']['Description'])
  return { 
    'isBase64Encoded': True,
    'statusCode': 200,
    'body': '',
    'headers': {
       'Content-Type': 'application/json', 
       'Access-Control-Allow-Origin': '*' 
   }
  }
