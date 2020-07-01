from __future__ import print_function
from datetime import datetime
import httplib2
from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
import pytz
SCOPES = ['https://www.googleapis.com/auth/calendar']
FLOW = OAuth2WebServerFlow(
    client_id='73558912455-smu6u0uha6c2t56n2sigrp76imm2p35j.apps.googleusercontent.com',
    client_secret='0X_IKOiJbLIU_E5gN3NefNns',
    scope=['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/contacts.readonly'],
    user_agent='Smart assistant box')
storage1 = Storage('info4.dat')
credentials = storage1.get()
if credentials is None or credentials.invalid == True:
  credentials = tools.run_flow(FLOW, storage1)
print(credentials)
# Create an httplib2.Http object to handle our HTTP requests and
# authorize it with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)
service = build('calendar', 'v3', http=http)
people_service = build(serviceName='people', version='v1', http=http)

utt = ("affich the events of 2020-06-20 00:00:00")
list = utt.split(" of ")
date = list[1]
sttdt  = datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
dx = pytz.utc.localize(sttdt)
datew = dx.isoformat("T")

print (datew)
now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
events_result = service.events().list(calendarId='primary', timeMin=now,singleEvents=True,orderBy='startTime',maxResults=10).execute()
events = events_result.get('items', [])
if not events:
    print("notEvent")

for event in events:
    summary = event['summary']
    eventstart = event['start']['dateTime']
    eventend = event['end']['dateTime']
    attendee = event['attendees']

    print("the event",summary,"starts",eventstart,"ends",eventend)