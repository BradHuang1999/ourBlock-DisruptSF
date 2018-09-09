import boto3
import rethinkdb as r 
import json
def upload(event, context):
	r.connect('52.87.241.222', 28015, user='admin',password='').repl()
	eventbody1 = json.dumps(event)
	eventbody = json.loads(eventbody1)
	report = {}
	defaults = {
    'lat': 0,
    'lon': 0,
    'time': 0,
    'privacy': "public",
    'reportingUser': "system",
    'anonymous': False,
    'message': "",
    'category': "other"
  	}
	for key in defaults:
		if key not in eventbody:
			eventbody[key] = defaults[key]
	
	report = {i:eventbody[i] for i in eventbody if i in defaults}

	r.db("ourblock").table("reportlog").insert([report]).run()
	return report
	



#r.db("ourblock").table("reportlog").delete().run()