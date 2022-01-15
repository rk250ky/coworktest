import time
import uuid
import datetime
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account

service_account_email_address = 'coworkreservationcalendar@coworkreservation.iam.gserviceaccount.com'

from app.daos import event_dao




def get_other_service(api_name, api_version, scopes, key_file_location):

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service

#hento ide cez domain delegation
def  get_service (api_name, api_version, scopes, key_file_location, mask):

    credentials = service_account.Credentials.from_service_account_file(key_file_location, scopes=scopes)

    delegated_credentials = credentials.with_subject(mask)

    service = build(api_name, api_version, credentials=delegated_credentials)
    return service






import os
from pprint import pprint



API_NAME='calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']
location  = os.path.dirname(os.path.abspath(__file__)) +'/coworkreservation-213a4920386a.json'
Mask = 'coworkreservationcalendar@coworkreservation.iam.gserviceaccount.com'



calendar_id_test = 'inkk68nqv1fc68gcuv3qnlj9k0@group.calendar.google.com'
calendar_id_resourses = 'c_bv5katfn6vvkho2k7ve8svv23c@group.calendar.google.com'

#object for service account with Domain Wide Delegation
service = get_service(API_NAME,API_VERSION,SCOPES,location,Mask)
# object for service account
services = get_other_service(API_NAME,API_VERSION,SCOPES,location)

#print(dir(service))

# request_body={
#     'summary' :'Test'
# }

def get_all_calendars_names():
    response = service.calendarList().list().execute()
    calendar_name_list = []
    for i in range(len(response)):
        calendar_name_list.append(response.get('items')[i]['summary'])
    return calendar_name_list

def get_all_calendars():
    response = service.calendarList().list().execute()
    return response

def insert_calendar(id):    #insert shared db without needed accept
    calendar_list_entry = {
        'id': id
    }

    created_calendar_list_entry = service.calendarList().insert(body=calendar_list_entry).execute()
    return created_calendar_list_entry['summary']


def get_all_events_names(calendar_id):
    list_of_events=[]
    events = service.events().list(calendarId=calendar_id).execute()
    for event in events['items']:
        if check_if_event_has_summary(event):
            list_of_events.append(event['summary'])
        else:
            list_of_events.append('None')
    return list_of_events


def get_all_events(calendar_id):
    events = service.events().list(calendarId=calendar_id).execute()
    return events

def create_calendar(request_body):
     response = service.calendars().insert(body=request_body).execute()      # create new calendar
     return response



def check_if_event_has_summary(event):
    if event.get('summary') == None :
        return False
    else:
        return True

def import_event(request_body,calendarID):
    imported_event = service.events().import_(calendarId=calendarID, body=request_body).execute()
    return imported_event

def create_event(summary,calendar_id):
    body = {
        'summary': summary,
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': '2021-11-28T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2021-11-28T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }


    event = service.events().insert(calendarId=calendar_id, body=body).execute()
    return event


def insert_role_on_calendar(calendarID,user,email):
    request_body = {
        'scope': {
            'type': user,
            'value': email,
        },
        'role': 'writer'
    }

    created_rule = service.acl().insert(calendarId=calendarID, body=request_body).execute()


def getlistintodb(list_json_of_events):
    for list_json_of_events in list_json_of_events['items']:
        print((list_json_of_events['id'] + ',' + list_json_of_events['updated']))
        # hentu sa pri pridavanie do db momentalne to nieje preto lebo tam terba menit veci v db

    return None



def get_new_events(id):
    updated_events = get_all_events(id)
    db = 'ctd2b1mfsviq0icbau413acu5c' # tu su eventy z db v danom kalendari pod id
    changed_id = []
    for updated_events in updated_events['items']:
        if updated_events['id'] in db:
            print('here')
            continue
        else:
            changed_id = updated_events['id']
            print(changed_id)

    return  None


def get_deleted_id(id): # treba cekovat pocet eventov v db a na internete
    updated_events = get_all_events(id)
    db = 'ctd2b1mfsviq0icbau413acu5c' # tu su eventy z db v danom kalendari pod id
    changed_id = []
    for updated_events in updated_events['items']:
        if updated_events['id'] in db:
            print('here')
            continue
        else:
            changed_id = updated_events['id']
            print("changed events:" + changed_id)



def add_events_to_db(id):
    updated_events = get_all_events(id)
    get_calendar_id = 1
    get_tenant_id = 1
    for updated_events in updated_events['items']:
        calendar_id = get_calendar_id # hento treba urobit tak ze id = id vrati id zaznamu
        room_id = updated_events['location']  # hento treba urobit tak ze meno = meno vrati id
        name = updated_events['summary']
        start =datetime.datetime.strptime(change_to_db(updated_events['start']['dateTime']), '%Y-%m-%dT%H:%M:%S')
        end = datetime.datetime.strptime(change_to_db(updated_events['end']['dateTime']), '%Y-%m-%dT%H:%M:%S')
        google_id = id
        tenant_id =get_tenant_id
        updated= updated_events['updated']
        break

    # print(calendar_id)
    # print(room_id)
    # print(name)
    # print(start)
    # print(end)
    # print(google_id)
    # print(tenant_id)
    # print(updated)
    pprint(event_dao.get_count_events_from_calendar_id("11"))


def change_to_db(data):
    data = data.split("+")
    return data[0]




def createhook(name):
    try:
        time_to_unix =  str((time.time() * 1000)+10)
    except:
        time_to_unix = str(0)
        pprint('Error on unix time')

    body= {
        "id": str(uuid.uuid4()),
        "type": "web_hook",
        "address": "https://coworkapp.me/tests",


    }
    #return  service.events().watch(calendarId= name, body = body).execute()








def closehook(id,resourceid):
    body = {
        'id': id,
        'resourceId': resourceid,

    }
    print(service.channels().stop(body=body).execute())


import json


def print_notification(entry):
    print(json.dumps(entry))
    import sys
    sys.stdout.flush()









# pprint('I am still here ')


# print_notification(" ")
# get_new_events(('3cmm3tsjhi70hgvk1j9p67k5r0@group.calendar.google.com'))
#pprint(create_event('test','3cmm3tsjhi70hgvk1j9p67k5r0@group.calendar.google.com'))
# pprint(get_all_calendars())
# print(closehook('a7407511-832e-4c65-8f49-f11e198d8c7c','lGFADe716IaqF4NRWk785rkrF_c'))
#print(createhook('2livateegthoron91afp2tg054@group.calendar.google.com'))
# pprint('halo')
#add_events_to_db('3cmm3tsjhi70hgvk1j9p67k5r0@group.calendar.google.com')








