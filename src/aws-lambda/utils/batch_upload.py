import boto3
from elasticsearch import Elasticsearch,RequestsHttpConnection
import pandas as pd
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
    
def make_str(line):
  return json.dumps(line.to_dict())
  
def many_append(arr,*args):
  for arg in args:
    arr.append(arg)
    
es = connectES('search-hacktps-2xwfbumjkznhuydichzbdudpe4.us-east-2.es.amazonaws.com') #add endpoint
df = pd.read_csv('sample.csv')
df = df.drop('Unnamed: 0',axis=1)
body = []
df.apply(lambda x: many_append(body,'{"index":{}}',make_str(x)),axis=1)
body = '\n'.join(body)+'\n'
es.bulk(body=body,index='data',doc_type='crime')