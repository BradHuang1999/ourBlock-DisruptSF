from flask import Flask,render_template,request,Response
from model import predict
import os
import requests
import json

app = Flask(__name__)
module_dir = os.path.abspath(os.path.dirname(__file__))
log_path = os.path.join(module_dir,'log.txt')

@app.route('/post',methods=['POST','OPTIONS'])
def post():
  if request.method=='POST':
    form = request.form.to_dict()
    if len(form.keys())==0:
      form = json.loads(request.data)
    classified = predict(form['message'])
    form['category'] = classified[0]
    #requests.post('https://wx44n042ha.execute-api.us-east-1.amazonaws.com/alpha/ourblockreportloglambda',json=data)
    requests.post('https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/post',json=form)
    with open(log_path,'a') as file:
      file.write(str(form)+'\n')
  resp = Response('')
  resp.headers['Access-Control-Allow-Origin'] = '*'
  resp.headers["Access-Control-Allow-Headers"] = 'Origin, X-Requested-With, Content-Type, Accept'
  return resp

@app.route('/')
def get():
  return 'hello world'

  '''
  print(request.form)
  print(type(request.form))
  form = ast.literal_eval(list(dict(request.form).keys())[0])
  try:
    classified,confidence = classify(form['Description'])[0]
  except Exception as e:
    print(e)
    classified,confidence = '',0
  data = form
  data['Class'] = classified
  data['Confidence'] = float(confidence)
  print(data['Class'],data['Confidence'])
  print(form)
  sendCrime(float(form['Latitude']),float(form['Longitude']),form['Class'])
  requests.post('https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/post',json=data)
  resp = Response('')
  resp.headers['Access-Control-Allow-Origin'] = '*'
  return resp
  '''
