# API Resources #

Searching for records: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/search

* Input arguments: {"query": query_string} or {"query": ""} to retrieve all records

* Output results: data with coordinates, description, other relevant information

Adding a new record: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/post

* Input arguments: {"body": body_dict}, which can be any data dictionary

* Output results: none

Sending a message: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/send

* Input arguments: {"id": user_id, "body": message}

* Output results: none

Receiving all new messages: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/notif

* Input arguments: {"id": user_id}

* Output results: list of all message contents to user since last read
