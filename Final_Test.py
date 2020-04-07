from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
FLOW = OAuth2WebServerFlow(
    client_id='1019838388650-nt1mfumr3cltemeq7js8mjitn7a2kuu7.apps.googleusercontent.com',
    client_secret='rx7eaJ-13TiHqOWIiF-Bxu4L',
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
            'client_secret_creds.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
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
results= people_service.people().connections().list(resourceName='people/me', pageSize=100, personFields='names,emailAddresses',fields='connections,totalItems,nextSyncToken').execute()
connections = results.get('connections', [])
print (connections)


    # la liste des evenements à venir
#page_token = None
#while True:
    #events = service.events().list(calendarId='primary', pageToken=page_token).execute()
    #for e in events['items']:
        #print(e['summary'])
    #page_token = events.get('nextPageToken')
    #if not page_token:
        #break
#getting contacts emails and names in two lists nameliste and adsmails
nameListe = []
adsmails =[]
attendee=[]
exist = False
for person in connections:
    emails = person.get('emailAddresses', [])
    names = person.get('names', [])
    adsmails.append(emails[0].get('value'))
    nameListe.append(names[0].get('displayName'))
x=input("donner le nombre des invités")
n=int(x)
print(n)
j=0
while j<n:
    x = input("donner le nom de l'invite")
    for l in range(0,len(nameListe)):
        if x == nameListe[l]:
            print ("personne trouvée")
            exist = True
            mail=adsmails[l]
            attendee.append(mail)
            print("listedes attendees",attendee)
            #on va verifier la disponibilité de chaque invité

            body = {
                "timeMin": '2015-05-28T09:00:00-07:00',
                "timeMax": '2015-07-28T09:00:00-07:00',
                "timeZone": 'US/Central',
                "items": [{"id": mail}]
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
        else:
            exist= False
    if exist == False:
        print(" la personne n'est pas trouvé")
    j+=1

print("liste des attendees est:",attendee)
attendeess = []
for i in range(len(attendee)):
    email = {'email': attendee[i]}
    attendeess.append(email)
print(attendeess)
event = {
    'summary': 'Google I/O 2020',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
        'dateTime': '2020-05-28T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': '2020-05-28T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
    },
    'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
    ],
    'attendees':attendeess,
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
        ],
    },
}

event = service.events().insert(calendarId='primary', body=event).execute()
print ('Event created: %s' % (event.get('htmlLink')))


