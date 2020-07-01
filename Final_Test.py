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
UTC_TZ = u'+00:00'
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
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
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
storage = Storage('info.dat')
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


    # la liste des evenements à venir
#page_token = None
#while True:
    #events = service.events().list(calendarId='primary', pageToken=page_token).execute()
    #for e in events['items']:
        #print(e['summary'])
    #page_token = events.get('nextPageToken')
    #if not page_token:
        #break
# get calendars id
page_token = None
while True:
  calendar_list = service.calendarList().list(pageToken=page_token).execute()
  for calendar_list_entry in calendar_list['items']:
      print("calendars id:",calendar_list_entry["id"])
  page_token = calendar_list.get('nextPageToken')
  if not page_token:
    break
#getting contacts emails and names in two lists nameliste and adsmails

nameListe = []
adsmails =[]
eventlist=[]
attendee=[]

#trouver connections :
for person in connections:
    emails = person.get('emailAddresses', [])
    print("email",emails)
    names = person.get('names', [])
    print("name",names)

    #event_pers= person.get('events',[])
    #print("event",events)
    adsmails.append(emails[0].get('value'))
    print(adsmails)
    nameListe.append(names[0].get('displayName'))
    print(nameListe)

    #a ={}
    #a ["summary"] =event_pers[0].get('summary')
    #a["created"]=event_pers[0].get('created')
    #a["updated"] = event_pers[0].get('updated')

    #eventlist.append(a)
      
#print("evenements",eventlist)

x=input("donner le nombre des invités")
n=int(x)
print(n)
local_time = pytz.timezone("UTC")
w = input("donner la date de cet evenement")
sttdt  = datetime.strptime(w,'%Y-%m-%d %H:%M:%S')
dx = pytz.utc.localize(sttdt)
datew = dx.isoformat("T")
print(datew)

dmin = input("donner la date de debut")
#rendre la chaine dmin de type datetime
startdt  = datetime.strptime(dmin,'%Y-%m-%d %H:%M:%S')
#rendre startdt de type json avec la format acceptee par google api
local_datetime1 = local_time.localize(startdt, is_dst=None)
utc_datetime1 = local_datetime1.astimezone(pytz.utc)
datestart = utc_datetime1.isoformat("T")
dmax = input("donner la date de fin")
enddt = datetime.strptime(dmax,'%Y-%m-%d %H:%M:%S')
local_datetime2 = local_time.localize(enddt, is_dst=None)
utc_datetime2 = local_datetime2.astimezone(pytz.utc)
datend= utc_datetime2.isoformat("T")
print(datestart)

j=0
while j<n:
    exist = False
    x = input("donner le nom de l'invite")
    for l in range(0,len(nameListe)):
        if x == nameListe[l]:
            print ("personne trouvée")
            exist = True
            mail=adsmails[l]
            attendee.append(mail)
            print("listedes attendees",attendee)

            # on va verifier la disponibilité de chaque invité#on va verifier la disponibilité de chaque invité
            #methode1
            #events_result = service.events().list(calendarId=mail, timeMin=datew,timeMax=datend,
                                                  #singleEvents=True,
                                                  #orderBy='startTime').execute()
            #events = events_result.get('items', [])

            #if not events:
                #print('the attendee is free')
            #else :
                #print('the attendee is busy ')
            #methode2
            body = {
                "timeMin": datew,
                "timeMax": datend,
                "timeZone": 'US/Central',
                "items": [{"id": mail}]
            }
            print (body.get("timeMin"))
            eventsResult = service.freebusy().query(body=body).execute()
            cal_dict = eventsResult[u'calendars']
            print(cal_dict)
            for cal_name in cal_dict:
                print(cal_name, ':', cal_dict[cal_name])
                statut = cal_dict[cal_name]
                bsy=0
                for i in statut:

                    if (i == 'busy' and statut[i] == []):
                        print("free")



                    elif (i == 'busy' and statut[i] != []):
                        print('busy')
                        bsy+=1

    if exist==False:
        print(" la personne n'est pas trouvé")
    j+=1
if bsy!=0:
    rech=input("voulez vous que je vous suggere une date min et date max commune")
    if rech=='yes':
        print(body)



print("liste des attendees est:",attendee)
attendeess = []
for i in range(len(attendee)):
    email = {'email': attendee[i]}
    attendeess.append(email)
print(attendeess)
notification=input("voulez vous envoyer une notification")
if notification == 'yes':
    notif = True,
else:
    notif = False
 #liste des emails de toutes les salles de focus
freerooms =[]
freemails=[]
nameroom =["Midoun meeting room","Aiguilles Meeting Room","Barrouta Meeting Room","Kantaoui Meeting Room","Gorges Meeting Room","Ichkeul Meeting Room","Khemir Meeting Room","Tamaghza Meeting Room","Friguia Meeting Room","Ksour Meeting Room","Medeina Meeting Room","Thyna Meeting Room"]
emailroom=["focus-corporation.com_3436373433373035363932@resource.calendar.google.com","focus-corporation.com_3132323634363237333835@resource.calendar.google.com","focus-corporation.com_3335353934333838383834@resource.calendar.google.com","focus-corporation.com_3335343331353831343533@resource.calendar.google.com","focus-corporation.com_3436383331343336343130@resource.calendar.google.com","focus-corporation.com_36323631393136363531@resource.calendar.google.com","focus-corporation.com_3935343631343936373336@resource.calendar.google.com","focus-corporation.com_3739333735323735393039@resource.calendar.google.com","focus-corporation.com_3132343934363632383933@resource.calendar.google.com","focus-corporation.com_@resource.calendar.google.com", "focus-corporation.com_@resource.calendar.google.com","focus-corporation.com_@resource.calendar.google.com"]
for i in range(0,len(emailroom)):
    body = {
        "timeMin": datew,
        "timeMax": datend,
        "timeZone": 'US/Central',
        "items": [{"id":emailroom[i]}]
    }
    roomResult = service.freebusy().query(body=body).execute()
    room_dict = roomResult[u'calendars']
    print(room_dict)
    for cal_room in room_dict:
        print(cal_room, ':', room_dict[cal_room])
        case = room_dict[cal_room]
        for j in case:
            if (j == 'busy' and case[j] == []):
                print("free")
                #la liste freerooms va prendre  les noms des salles free
                freerooms.append(nameroom[i])
                freemails.append(emailroom[i])

            elif (j == 'busy' and case[j] != []):
                print('busy')
print(freerooms)
print(freemails)
reservation = input('do you need to make a reservation for a meeting room? Yes or No?')
if reservation == 'yes':
    print("les salles disponibles a cette date sont",freerooms)
    salle=input('quelle salle choisissez vous')
    print (salle)
    for i in range(0,len(freerooms)):
        if(freerooms[i] == salle):
            attendeess.append({'email': freemails[i]})
elif reservation == 'no':
    salle =''
print(attendeess)

#affichage des salles disponibles a cette date

event = {
    'summary': 'title of the event',
    'location': salle,
    'description': 'test event',
    'start': {
        'dateTime': datestart,
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': datend,
        'timeZone': 'America/Los_Angeles',
    },
    'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=1'
    ],
    'attendees':attendeess,
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
        ],
    },
   # 'conferenceData':{
        #'conferenceDataVersion':1,
        #'conferenceSolutionKey.type':"hangoutsMeet",
        #'createRequest':'',

    #},

}

event = service.events().insert(calendarId='primary',sendNotifications=notif, body=event).execute()
print ('Event created: %s' % (event.get('htmlLink')))
loc =input("donner la nouvelle location")
for j, e in enumerate(nameroom):
    if salle == e:
        deletemail = emailroom[j]
        email = {'email': deletemail}
        print(email)
for i in attendeess:
    if i == email:
        print(i)
        attendeess.remove(i)
        print("attedees",attendeess)

for i in range(len(nameroom)):
    if nameroom[i] == loc:
        roommail = emailroom[i]
print('lemail de la nouvelle sall',roommail)
body = {
    "timeMin": datestart,
    "timeMax": datend,
    "timeZone": 'America/Los_Angeles',
    "items": [{"id": roommail}]
}
eventsResult = service.freebusy().query(body=body).execute()
cal_dict = eventsResult[u'calendars']
print(cal_dict)
for cal_name in cal_dict:
    print(cal_name, ':', cal_dict[cal_name])
    statut = cal_dict[cal_name]
    for i in statut:
        if (i == 'busy' and statut[i] == []):
            x= True

            # ajouter l'email de x ala liste des attendee
        elif (i == 'busy' and statut[i] != []):
            x= False

if x == True:
    email = {'email': roommail}
    attendeess.append(email)
    eventup = {
        'location': loc,
        'attendees': attendeess,
    }
    service.events().patch(calendarId='primary', eventId=event['id'],
                           sendNotifications=True, body=eventup).execute()
else:
    print('room busy')

name = input("what is the attendee's name?")
for j, e in enumerate(nameListe):
    if name == e:
        deletemail = adsmails[j]
        email = {'email': deletemail}
        print(email)
for i in attendeess:
    if i == email:
        print(i)
        attendeess.remove(i)
eventup = {
    'attendees': attendeess,
}
service.events().patch(calendarId='primary', eventId=event['id'],
                           sendNotifications=True, body=eventup).execute()
name = input("what is the attendee's name?")
for j, e in enumerate(nameListe):
    if name == e:
        addemail = adsmails[j]
        email = {'email': addemail}
        print(email)
body = {
    "timeMin": datestart,
    "timeMax": datend,
    "timeZone": 'America/Los_Angeles',
    "items": [{"id": addemail}]
}
eventsResult = service.freebusy().query(body=body).execute()
cal_dict = eventsResult[u'calendars']
print(cal_dict)
for cal_name in cal_dict:
    print(cal_name, ':', cal_dict[cal_name])
    statut = cal_dict[cal_name]
    for i in statut:
        if (i == 'busy' and statut[i] == []):
            x= True

            # ajouter l'email de x ala liste des attendee
        elif (i == 'busy' and statut[i] != []):
            x= False
if x == True:

    email = {'email': addemail}
    attendeess.append(email)
    eventup = {
        'attendees': attendeess,
    }
    service.events().patch(calendarId='primary', eventId=event['id'],
                           sendNotifications=True, body=eventup).execute()
