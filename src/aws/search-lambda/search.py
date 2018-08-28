import boto3
from elasticsearch import Elasticsearch,RequestsHttpConnection
import json
from math import cos,sqrt

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

def search(event,context):
  event = json.loads(event['body'])
  query_body = {
    'query':{
      'query_string':{
        'default_field':'message',
        'query':event['messageQuery'] if 'messageQuery' in event else ''
      }
    },
    'filter':{
      'bool':{
        'must':[
        ]
      }
    }
  }
  and_array = query_body['filter']['bool']['must']
  for key in event:
    if key in ['category','reportingUser']:
      and_array.append({'terms':{key:event[key]}})
    elif key in ['severity','time']:
      and_array.append({'range':{key:{'gte':event[key]}}})
    elif key=='location':
      if all([x in event[key] for x in ['lon','lat','radiusLon','radiusLat']]):
        lon,lat,rlon,rlat = [event[key][x] for x in ['lon','lat','radiusLon','radiusLat']]
        and_array.append({'range':{'lon':{'gte':lon-rlon,'lte':lon+rlon}}})
        and_array.append({'range':{'lat':{'gte':lat-rlat,'lte':lat+rlat}}})
    elif key=='select':
      query_body['_source'] = event['select']
  query_body['filter']['bool']['must'] = and_array
  data = es.search(index='data',doc_type='crime',size=10000,from_=0,body=query_body)
  def convert_coord_to_miles(lat1,lon1,lat2,lon2):
    #assumes roughly same latitude
    dx = abs(lat1-lat2)*69
    dy = cos(lat1*3.141592/180)*69*abs(lon1-lon2)
    return sqrt(dx**2+dy**2)
  if 'distance' in event['select']:
    for item in data['hits']['hits']:
      if 'lat' in item['_source'] and 'lon' in item['_source']:
        lat,lon = event['location']['lat'],event['location']['lon']
        item['_source']['distance'] = convert_coord_to_miles(item['_source']['lat'],item['_source']['lon'],lat,lon)
  #incorporate vishal's code
  return { 
    'isBase64Encoded': True,
    'statusCode': 200,
    'body': json.dumps(data['hits']['hits']),
    'headers': {
       'Content-Type': 'application/json', 
       'Access-Control-Allow-Origin': '*' 
    }
  }
