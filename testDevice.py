from __future__ import print_function
import json
import sys
from adapt.intent import IntentBuilder
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

import string
import pytz
local_time = pytz.timezone("UTC")

# in the raspberry we add __main__.py for the authorization
UTC_TZ = u'+00:00'
FLOW = OAuth2WebServerFlow(
    client_id='73558912455-smu6u0uha6c2t56n2sigrp76imm2p35j.apps.googleusercontent.com',
    client_secret='0X_IKOiJbLIU_E5gN3NefNns',
    scope=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/contacts.readonly',
           'https://www.googleapis.com/auth/admin.directory.resource.calendar'],
    user_agent='Smart assistant box')

def utc_offset(self):
    return timedelta(seconds=self.location['timezone']['offset'] / 1000)

def recherche(list1, list2, l):
    for i in range(len(list1)):
        if list1[i] == l:
            mail = list2[i]
    return mail

def rechDevice(d, freedeviceslist):
    l=[]
    for i in freedeviceslist:
        print(i)
        if d in i:
            l.append(i)

    return l

def freebusy(mail, datestart, datend, service):
    body = {
            "timeMin": datestart,
            "timeMax": datend,
            "timeZone": 'America/Los_Angeles',
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
                return True

                    # ajouter l'email de x ala liste des attendee
            elif (i == 'busy' and statut[i] != []):
                return False


def handle_device():
        storage1 = Storage('info5.dat')
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
        results = people_service.people().connections().list(resourceName='people/me', pageSize=100,
                                                             personFields='names,emailAddresses',
                                                             fields='connections,totalItems,nextSyncToken').execute()
        connections = results.get('connections', [])
        print("authorized")
        utt = "reservate a pc and keybozrd for 2020-07-01 11:00:00"
        print(utt)
        listdiv=[]
        liste1 = utt.split(" a ")
        liste2 = liste1[1].split(" for ")
        if ("and") in liste2[0]:
            listdiv = liste2[0].split(" and ")
        else:
            listdiv.append(liste2[0])
        print(listdiv)
        date1 = liste2[1]
        startdt = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
        local_datetime2 = local_time.localize(startdt, is_dst=None)
        utc_datetime2 = local_datetime2.astimezone(pytz.utc)
        datestart = utc_datetime2.isoformat("T")

        print(datestart)
        dmax = input("donner la date de fin")
        enddt = datetime.strptime(dmax, '%Y-%m-%d %H:%M:%S')
        local_datetime2 = local_time.localize(enddt, is_dst=None)
        utc_datetime2 = local_datetime2.astimezone(pytz.utc)
        dater = utc_datetime2.isoformat("T")

        nameListe = []
        adsmails = []
        # attendee est la liste des invités qui sont disponibles
        attendees = []

        for person in connections:
            emails = person.get('emailAddresses', [])
            names = person.get('names', [])
            adsmails.append(emails[0].get('value'))
            nameListe.append(names[0].get('displayName'))
        print(nameListe)
        print(adsmails)
        nameEmp = input('u tell me your name?')
        mailEmp = recherche(nameListe, adsmails, nameEmp)

        # service.list(customer='my_customer' , orderBy=None, pageToken=None, maxResults=None, query=None)
        # .get(customer=*, calendarResourceId=*)
        listD = ['FOCUS-RDC-PCFOCUS (1)']
        listDmails = ['c_1882n3ruihk0qj7nnpqdpqhl5h4um4glcpnm6tbj5lhmusjgdtp62t39dtn2sorfdk@resource.calendar.google.com']
        freeDevices = []
        freemails = []
        for i in range(len(listDmails)):
            x = freebusy(i, datestart, dater, service)
            if x == True:
                freeDevices.append(listD[i])
                freemails.append(listDmails[i])
        print(freemails)
        s = ",".join(freeDevices)
        print( 'free devices'+ s)
        for device in listdiv:
            l=[]
            for i in freeDevices:
                print(i)
                if device in i.lower():
                    l.append(i)
                    print(l)
            if l !=[]:
                print('the available devices are'+ s)
                choice = input('what is your choice?')
                email = recherche(freeDevices, freemails, choice)
                attendees.append({'email': email})
                summary = choice + "reservation for Mr/Ms" + nameEmp
                description = "Mr/Ms" + nameEmp + "'s email:" + mailEmp
                reservation = {
                    'summary': summary,
                    'description': description,
                    'location': 'Focus corporation',
                    'start': {
                        'dateTime': datestart,
                        'timeZone': 'America/Los_Angeles',
                    },
                    'end': {
                        'dateTime': dater,
                        'timeZone': 'America/Los_Angeles',
                    },
                    'recurrence': [
                        'RRULE:FREQ=DAILY;COUNT=1'
                    ],
                    'attendees': attendees,
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'email', 'minutes': 24 * 60},
                            {'method': 'popup', 'minutes': 10},
                        ],
                    },
                }
                reservation = service.events().insert(calendarId='primary', sendNotifications=True,
                                                      body=reservation).execute()
                print('Event created: %s' % (reservation.get('htmlLink')))
                print('deviceReservated')
            else:
                print('no available devices')


handle_device()