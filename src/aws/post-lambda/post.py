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
  es.index(index='data',doc_type='crime',body=event)
  '''
  try:
    query_dict = {
      'query': {
        'bool': {
          'must': [
            {
            'term': {
              'Year':event['Year']
            }
            },
            {
            'term': {
              'Month':event['Month']
            }
            },
            {
            'range': {
              'Day': {
                'gte':event['day']-3,
                'lte':event['day']
              }
            }
            },
            {
            'range': {
              'Latitude': {
                'gte':event['Latitude']-0.0005,
                'lte':event['Latitude']+0.0005
              }
            }
            },
            {
            'range': {
              'Longitude': {
                'gte':event['Longitude']-0.0005,
                'lte':event['Longitude']+0.0005
              }
            }
            },
            {
            'term': {
              'Class':event['Class']
            }
            }
          ]
        }
      }
    }
    num_results = es.search(index='data',doc_type='crime',size=0,body=query_dict)['hits']['total']
  except:
    num_results = 0
  if 'Class' not in event or event['Class'] in ['Assault','Homicide','Sexual Assault'] or (event['Confidence']>0.5 and num_results>1):
    requests.post('https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/send',data={'id':'_all','body':'Crime reported: '+event['Description'] if 'Description' in event else 'no description.'})
  #sendCrime(event['Latitude'],event['Longitude'],event['Description'])
  '''
  return { 
    'isBase64Encoded': True,
    'statusCode': 200,
    'body': '',
    'headers': {
       'Content-Type': 'application/json', 
       'Access-Control-Allow-Origin': '*' 
   }
  }
