import boto3
from elasticsearch import Elasticsearch,RequestsHttpConnection
import json
from math import cos,sqrt
from collections import defaultdict

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

weights = defaultdict(dict, {
    'police': defaultdict(float, {
        'distance': -0.1 / 1000,
        'category': 1,
        'time': -10 / (1000 * 1000 * 60 * 60 * 24),
        'upvotes': 0.1,
        'downvotes': -0.2,
        'followers': 0.2,
        'status': 1
    }),
    'civilian': defaultdict(float, {
        'distance': -1,
        'category': 1,
        'time': 1,
        'upvotes': 1,
        'downvotes': -1,
        'followers': 1, 
        'status': 1  
    })
})

categoryWeights = defaultdict(float, {
    "Larceny/Theft": 0.3,
    "Violence/Homicide": 1,
    "Mental Health/Bullying": 0.6,
    "Drug/Narcotics": 0.5,
    "Kidnapping": 0.9,
    "Traffic Violation": 0.4,
    "Sex Offences": 0.6,
    "other": 0.5
})

statusWeights = defaultdict(float, {
    "solved by police": 0.001,
    "solved by public": 0.01,
    "in progress": 0.1,
    "pending": 1
})

def convert_coord_to_miles(lat1,lon1,lat2,lon2):
  #assumes roughly same latitude
  dx = abs(lat1-lat2)*69
  dy = cos(lat1*3.141592/180)*69*abs(lon1-lon2)
  return sqrt(dx**2+dy**2)

def convert_coord_to_meters(lat1, lon1, lat2, lon2):
  return 1609.34 * convert_coord_to_miles(lat1,lon1,lat2,lon2)

def getSeverity(role,currentTime,currLat,currLon,doc):
  categoryCoef = categoryWeights[doc['category']]
  statusCoef = statusWeights[doc['status']]
  distance = convert_coord_to_meters(currLat,currLon,doc['lat'],doc['lon'])
  doc['distance'] = distance
  arr = [
    weights[role]['status']*statusCoef,
    weights[role]['distance']*distance,
    weights[role]['category']*categoryCoef,
    weights[role]['time']*(currentTime-doc['time']),
    weights[role]['upvotes']*doc['upvoterCount'],
    weights[role]['downvotes']*doc['downvoterCount'],
    weights[role]['followers']*doc['followerCount']
  ]
  severity = sum(arr)
  doc['severity'] = severity
  return severity

def search(event,context):
  event = json.loads(event['body'])
  if 'reportId' in event:
    source_doc = es.get(index='data',doc_type='crime',id=event['reportId'])['_source']
    source_doc['_id'] = event['reportId']
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
    if key in ['category','reportingUser','status']:
      and_array.append({'term':{key:event[key]}})
    elif key in ['time','upvoterCount','downvoterCount','followerCount','commentCount']:
      and_array.append({'range':{key:{'gte':event[key]}}})
    elif key=='location':
      if all([x in event[key] for x in ['lonMin','lonMax','latMin','latMax']]):
        lonmin,lonmax,latmin,latmax = [event[key][x] for x in ['lonMin','lonMax','latMin','latMax']]
        and_array.append({'range':{'lon':{'gte':lonmin,'lte':lonmax}}})
        and_array.append({'range':{'lat':{'gte':latmin,'lte':latmax}}})
    elif key=='select' and 'severity' not in event:
      query_body['_source'] = event['select']
  query_body['query']['bool']['filter'] = and_array
  limit = 10000 if 'limit' not in event or 'severity' in event else min(10000,event['limit'])
  data = es.search(index='data',doc_type='crime',size=limit,from_=0,body=query_body)
  if ('select' in event and 'distance' in event['select']):
    for item in data['hits']['hits']:
      if 'lat' in item['_source'] and 'lon' in item['_source']:
        lat,lon = event['location']['lat'],event['location']['lon']
        item['_source']['distance'] = convert_coord_to_miles(item['_source']['lat'],item['_source']['lon'],lat,lon)
  #incorporate vishal's code
  output = []
  for item in data['hits']['hits']:
    row = item['_source']
    row['_id'] = item['_id']
    for a,b in zip(['upvoters','downvoters','followers'],['upvoterCount','downvoterCount','followerCount']):
      if a in row:
        row[a] = list(set(row[a]))
        if b in row:
          row[b] = len(row[a])
    output.append(row)
  if all([x in event for x in ['severity','currentTime','currLat','currLon','role']]):
    output = sorted(output,key=lambda x: getSeverity(event['role'],event['currentTime'],event['currLat'],event['currLon'],x),reverse=True)
    if 'select' in event:
      event['select'].extend(['_id','severity','distance'])
      for i,item in enumerate(output):
        output[i] = {key:item[key] for key in item if key in event['select']}
    if 'limit' in event:
      output = output[:event['limit']]
  return { 
    'isBase64Encoded': True,
    'statusCode': 200,
    'body': json.dumps(output),
    'headers': {
       'Content-Type': 'application/json', 
       'Access-Control-Allow-Origin': '*' 
    }
  }
