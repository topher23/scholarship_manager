import json
from time import sleep

import requests

from database import Database
from scholarship import ScholarshipFilter

db = Database()
mailgun_private_key = ""

#build golden query
query=ScholarshipFilter()
query.amount_greater_than = 500


def email_send(result):
    rows = []
    for row in result:
        rows.append(json.dumps(row.clean_as_dict()))
    text = "Hello, \nThere has been a new scholarship added that matches your filter! Below are a" \
           "list of all the scholarships that match your filter including the new one. Check out " \
           "all of our scholarships available on our website.\n\n" + "\n".join(rows) + "\n\nRegards, \n" \
           "Christopher Dorick"

    return requests.post(
        "https://api.mailgun.net/v3/sandboxb65cde344acd4820963ca79eec33db5c.mailgun.org/messages",
        auth=("api", mailgun_private_key),
        data={"from": "ScholarshipService@test.com",
            "to": "topher23@vt.edu",
            "subject": "New Scholarships! 2",
            "text": text})

size = -1
#event loop
while(1):

    query_result = db.fetch_specific(query)
    fresh_size = len(query_result)

    #first run
    if size < 0:
        size = fresh_size
        print("initial run")
    elif fresh_size > size:
        #send email
        size = fresh_size
        print("new content! sending email then sleeping for 60s")
        email_send(query_result)
    else:
        email_send(query_result)
        print("no new content. Sleeping for 60s")

    sleep(60)



