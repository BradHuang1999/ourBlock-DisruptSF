import boto3
import json

sqs = boto3.resource('sqs')

def send(event,context):
  event = json.loads(event['body'])
  try:
    sqs.create_queue(QueueName=event['id'])
  except Exception as e:
    print(e)
    pass
  queue = sqs.get_queue_by_name(QueueName=event['id'])
  response = queue.send_message(MessageBody=event['body'])
  return { 
      'isBase64Encoded': True,
      'statusCode': 200,
      'body': '',
      'headers': {
         'Content-Type': 'application/json', 
         'Access-Control-Allow-Origin': '*' 
       }
       }