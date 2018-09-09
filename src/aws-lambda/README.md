# API Resources #

Searching for records: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/search

* Input arguments: see https://github.com/BradHuang1999/ourBlock-DisruptSF/projects/2#card-12325211 and https://github.com/BradHuang1999/ourBlock-DisruptSF/projects/2#card-12421360 (time must be Unix timestamp, i.e. milliseconds since the epoch, returned by Javascript's date.now())

* Output results: matched records, JSON encoded

Adding a new record: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/post

* Input arguments: any data dictionary, see https://github.com/BradHuang1999/ourBlock-DisruptSF/ projects/2#card-12325051 (time must be Unix timestamp, i.e. milliseconds since the epoch, returned by Javascript's date.now())

* Output results: none

Sending a message: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/send

* Input arguments: {"id": send\_to\_user\_id, "user": sent\_from\_user\_id, "type": one of \[New Comment, Status Update, New Report, My Report\], "report": message of the report which generated the message, "body": message}

* Output results: none

Receiving all new messages: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/notif

* Input arguments: {"id": user\_id}

* Output results: list of all message contents to user since last read, JSON encoded

Upvote, downvote, or follow a report: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/interact

* Input arguments: {"userId": user\_id, "reportId": report\_id, "action": one of \["upvote","downvote","follow"\]}

* Output results: none

Comment on a report: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/comment

* Input arguments: {"userId": user\_id, "reportId": report\_id, "message": comment\_message, "timestamp": current\_time} (timestamp must be Unix timestamp, i.e. milliseconds since the epoch, returned by Javascript's date.now())

* Output results: none

Update report: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/update

* Input arguments: {"reportId": report\_id, "value": value\_to\_assign, "field": field\_to\_update} (values accepted for "status" field: \["pending","in progress","solved by public","solved by police"\]; values accepted for "privacy" field: \["private","public"\])

* Output results: none

Get summary stats: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/stats

* Input arguments: none

* Output results: a data dictionary with one key for each possible status, indicating the number of reports with that status in the past week, as well as a key "total", which is the total number of reports in the last week, JSON encoded

Bulk upload: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/bulk-upload

* Input arguments: \[{"column1":"value1","column2":"value2",...},{"column1":"value3","column2":"value4",...},...\]

* Output results: none

Token: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/token

* Input arguments: {"userId": user\_id, "action": optional argument, if included will increment token count by 1}

* Output results: the number of tokens belonging to a user

Clear token for all users: https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/clear-token

* Input arguments: none

* Output results: none
