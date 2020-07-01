from __future__ import print_function
from datetime import datetime, timedelta
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import httplib2
from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
import pytz
import json
import sys
import re
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.engine import IntentDeterminationEngine
UTC_TZ = u'+00:00'
tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)
engine = IntentDeterminationEngine()

#authorise
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
FLOW = OAuth2WebServerFlow(
    client_id='73558912455-smu6u0uha6c2t56n2sigrp76imm2p35j.apps.googleusercontent.com',
    client_secret='0X_IKOiJbLIU_E5gN3NefNns',
    scope='https://www.googleapis.com/auth/contacts.readonly',
    user_agent='Smart assistant box')
"""Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
if os.path.exists('token.pickle'):
     with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'c:/Users/USER/PycharmProjects/TestCalendar/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open('c:/Users/USER/PycharmProjects/TestCalendar/token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])

    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.
# If the Credentials don't exist or are invalid, run through the
# installed application flow. The Storage object will ensure that,
# if successful, the good Credentials will get written back to a
# file.
storage = Storage('c:/Users/USER/PycharmProjects/TestCalendar/info.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = tools.run_flow(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and
# authorize it with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. To get an API key for
# your application, visit the Google API Console
# and look at your application's credentials page.
people_service = build(serviceName='people', version='v1', http=http)
#To get the person information for any Google Account, use the following code:
#profile = people_service.people().get('people/me', pageSize=100, personFields='names,emailAddresses').execute()
# To get a list of people in the user's contacts,
#results = service.people().connections().list(resourceName='people/me',personFields='names,emailAddresses',fields='connections,totalItems,nextSyncToken').execute()
results= people_service.people().connections().list(resourceName='people/me', pageSize=100, personFields='names,emailAddresses,events',fields='connections,totalItems,nextSyncToken').execute()
connections = results.get('connections', [])
print ("connections:",connections)
#liste de personnes
nameliste= []
adsmails= []
for person in connections:
    emails = person.get('emailAddresses', [])

    adsmails.append(emails[0].get('value'))
    print(adsmails)
    names = person.get('names', [])

    nameliste.append(names[0].get('displayName'))
#liste des emails des salles
emailroom=["focus-corporation.com_3436373433373035363932@resource.calendar.google.com","focus-corporation.com_3132323634363237333835@resource.calendar.google.com","focus-corporation.com_3335353934333838383834@resource.calendar.google.com","focus-corporation.com_3335343331353831343533@resource.calendar.google.com","focus-corporation.com_3436383331343336343130@resource.calendar.google.com","focus-corporation.com_36323631393136363531@resource.calendar.google.com","focus-corporation.com_3935343631343936373336@resource.calendar.google.com","focus-corporation.com_3739333735323735393039@resource.calendar.google.com","focus-corporation.com_3132343934363632383933@resource.calendar.google.com","focus-corporation.com_@resource.calendar.google.com", "focus-corporation.com_@resource.calendar.google.com","focus-corporation.com_@resource.calendar.google.com"]

# la fonction recherche
def recherche(chaine,liste):
    i=0
    #x=None
    while i in range(len(liste)):
        if liste[i]==chaine :
            #x=i
            return (i)
            break
        else:
            i+=1
    #return (x)
#la fonction freebusy
def freebusy(idmail):
    body = {
        "timeMin": '2020-05-20T12:00:00+00:00',
        "timeMax": '2020-05-20T14:00:00+00:00',
        "timeZone": 'US/Central',
        "items": [{"id": idmail}]
    }
    eventsResult = service.freebusy().query(body=body).execute()
    cal_dict = eventsResult[u'calendars']
    print(cal_dict)
    for cal_name in cal_dict:
        print(cal_name, ':', cal_dict[cal_name])
        statut = cal_dict[cal_name]
        for i in statut:

            if (i == 'busy' and statut[i] == []):
                print("free")
            elif (i == 'busy' and statut[i] != []):
                print('busy')

# creating entities
person_keywords = nameliste
print(person_keywords)
for wk in person_keywords:
    engine.register_entity(wk, "PersonKeyword")

add_keywords = [
    'create',
    'add',
    'new',
    'make'
]
print(add_keywords)
for wk in add_keywords:
    engine.register_entity(wk, "AddKeyword")
event_keywords = [
    'appointment',
    'appointments',
    'meeting',
    'meetings',
    'meetup',
    'meetups',
    'event'
]
for wk in event_keywords:
    engine.register_entity(wk, "EventKeyword")
location_keywords = [
    'Midoune Room',
    'Aiguilles Room',
    'Barrouta Room',
    'Kantaoui Room',
    'Gorges Room',
    'Ichkeul Room',
    'Khemir Room',
    'Tamaghza Room',
    'Friguia Room',
    'Ksour Room',
    'Medeina Room',
    'Thyna Room'
]
for wk in location_keywords:
    engine.register_entity(wk, "LocationKeyword")
# creating intents
add_regex_keywords = ['{}(?P<Add>\S*)'.format(keyword)
                      for keyword in add_keywords]
event_regex_keywords = ['{} (?P<Event>(?:(?!with|in|the|).)*)'.format(keyword)
                        for keyword in event_keywords]

with_regex_keywords = ['{}(with)(?P<Person>\S*)'.format(keyword)
                      for keyword in person_keywords]
print(with_regex_keywords)
location_regex_keywords = ['{} (in) (?P<Location>\S*)(starts)'.format(keyword)
                           for keyword in location_keywords]

date_regex_keyword = '(?P<Date>\S*)'

# Register entities on engine
for regex in add_regex_keywords:
    engine.register_regex_entity(regex)
for regex in event_regex_keywords:
    engine.register_regex_entity(regex)
for regex in location_regex_keywords:
    engine.register_regex_entity(regex)
for regex in with_regex_keywords:
    engine.register_regex_entity(regex)
# construt an intent parser
add_event_intent = IntentBuilder('EventIntent') \
    .require('AddKeyword') \
    .require('EventKeyword') \
    .require('Personkeyword') \
    .optionally('LocationKeyword') \
    .optionally('Date') \
    .build()
engine.register_intent_parser(add_event_intent)
x='Add event with Hana Bouzid in Midoune Room starts 10 am'
for intent in engine.determine_intent(x):
    clist=[]
    alist = x.split("with ")
    print(alist)
    blist=alist[1].split(" in")
    lliste=blist[1].split("starts")
    print(blist)
    print(lliste)
    if("and")in blist[0]:
        clist = blist[0].split("and")
        print(clist)  # liste des attendees cités dans x
        print(type(clist))
    else :
        clist.append(blist[0])
        print(clist) #liste des attendees cités dans x
        print(type(clist))

    room = intent.get('LocationKeyword')
    print(room)
    print(type(room))
    pers = intent.get('Personkeyword')
    print(intent.get("utterance"))
    print(pers)
    #room
    indiceroom = recherche(room,location_keywords)
    print(indiceroom)
    idmailr=emailroom[indiceroom]
    freebusy(idmailr)
    # personne
    #indiceperson = recherche(pers,person_keywords)
    for i in clist:
        print(i)
        indiceperson = recherche(i, person_keywords)
        print("personn1", indiceperson)
        ind=person_keywords.index(i)
        print("personn", ind)
        for j, e in enumerate(person_keywords):
            if e == i:
                print(j)


    idmailp = adsmails[indiceperson]
    print(idmailp)

    # freebusy
    freebusy(idmailp)
    freebusy(idmailr)







