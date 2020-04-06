import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for
# installed applications.
#
# Go to the Google API Console, open your application's
# credentials page, and copy the client ID and client secret.
# Then paste them into the following code.
FLOW = OAuth2WebServerFlow(
    client_id='1019838388650-nt1mfumr3cltemeq7js8mjitn7a2kuu7.apps.googleusercontent.com',
    client_secret='rx7eaJ-13TiHqOWIiF-Bxu4L',
    scope='https://www.googleapis.com/auth/contacts.readonly',
    user_agent='Smart assistant box')

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


#getting contacts emails and names in two lists nameliste and adsmails
nameListe = []
adsmails =[]
exist = False
for person in connections:
    emails = person.get('emailAddresses', [])
    names = person.get('names', [])
    adsmails.append(emails[0].get('value'))
    nameListe.append(names[0].get('displayName'))
x= input ("donner le nom del l'invité")
for i in nameListe:
    if i == x :
        print ("personne trouvée")
        exist = True
        break
if exist == False :
    print(" la personne n'est pas trouvé")