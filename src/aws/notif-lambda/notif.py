import boto3
import json

def notif(event,context):
  event = json.loads(event['body'])
  sqs = boto3.resource('sqs')
  messages = []
  try:
    queue = sqs.get_queue_by_name(QueueName=event['id'])
    for message in queue.receive_messages():
      messages.append(message.body)
      message.delete()
  except:
    print(event['id'])
  try:
    all_queue = sqs.get_queue_by_name(QueueName='_all')
    for message in all_queue.receive_messages():
      messages.append(message.body)
      message.delete()
  except:
    print('_all')
  return { 
        'isBase64Encoded': True,
        'statusCode': 200,
        'body': json.dumps(messages),
        'headers': {
           'Content-Type': 'application/json', 
           'Access-Control-Allow-Origin': '*' 
       }
}