from flask import Flask,render_template,request,Response
from model import predict
import requests
import ast
import json

app = Flask(__name__)

@app.route('/post',methods=['POST'])
def post():
  form = dict(request.form)
  try:
    classified = predict(form['Description'][0])
  except Exception as e:
    print(e)
    classified = ''
  data = form
  data['Class'] = classified
  print(form)
  #requests.post('https://wx44n042ha.execute-api.us-east-1.amazonaws.com/alpha/ourblockreportloglambda',json=data)
  #requests.post('https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/post',json=data)
  resp = Response('')
  return resp

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
