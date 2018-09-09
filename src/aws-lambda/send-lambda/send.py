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
  user_id = event['id']
  del event['id']
  if 'type' not in 'event':
    if '__type__' in event:
      if 'Thanks for all your collaboration!' in event['body']:
        event['type'] = 'Status Update'
      else:
        event['type'] = 'New Comment'
      del event['__type__']
  queue = sqs.get_queue_by_name(QueueName=user_id)
  response = queue.send_message(MessageBody=json.dumps(event))
  return { 
      'isBase64Encoded': True,
      'statusCode': 200,
      'body': '',
      'headers': {
         'Content-Type': 'application/json', 
         'Access-Control-Allow-Origin': '*' 
       }
       }