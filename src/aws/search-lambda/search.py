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
  if 'reportId' in event:
    source_doc = es.get(index='data',doc_type='crime',id=event['reportId'])['_source']
    return { 
      'isBase64Encoded': True,
      'statusCode': 200,
      'body': json.dumps(source_doc),
      'headers': {
         'Content-Type': 'application/json', 
         'Access-Control-Allow-Origin': '*' 
      }
    }
  if 'select' in event:
    event['select'] = event['select'].split(' ')
  query_body = {
    'query':{
      'bool':{
        'filter':[
        ]
      }
    }
  }
  if 'messageQuery' not in event or event['messageQuery']=='':
    pass
  else:
    query_body['query']['bool']['must'] = [{
      'query_string': {
        'default_field':'message',
        'query':event['messageQuery']
      }
    }]
  and_array = query_body['query']['bool']['filter']
  for key in event:
    if key in ['category','reportingUser']:
      and_array.append({'term':{key:event[key]}})
    elif key in ['severity','time','upvoterCount','downvoterCount','followerCount','commentCount']:
      and_array.append({'range':{key:{'gte':event[key]}}})
    elif key=='location':
      if all([x in event[key] for x in ['lon','lat','radiusLon','radiusLat']]):
        lon,lat,rlon,rlat = [event[key][x] for x in ['lon','lat','radiusLon','radiusLat']]
        and_array.append({'range':{'lon':{'gte':lon-rlon,'lte':lon+rlon}}})
        and_array.append({'range':{'lat':{'gte':lat-rlat,'lte':lat+rlat}}})
    elif key=='select':
      query_body['_source'] = event['select']
  query_body['query']['bool']['filter'] = and_array
  data = es.search(index='data',doc_type='crime',size=10000,from_=0,body=query_body)
  def convert_coord_to_miles(lat1,lon1,lat2,lon2):
    #assumes roughly same latitude
    dx = abs(lat1-lat2)*69
    dy = cos(lat1*3.141592/180)*69*abs(lon1-lon2)
    return sqrt(dx**2+dy**2)
  if 'select' in event and 'distance' in event['select']:
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
