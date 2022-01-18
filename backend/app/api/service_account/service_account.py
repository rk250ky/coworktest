import time
import uuid
import datetime
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account

service_account_email_address = 'coworkreservationcalendar@coworkreservation.iam.gserviceaccount.com'

from app.daos import event_dao,room_dao,tenant_dao,calendar_dao




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

def delete_event(calendar_id,id):
    a = service.events().delete(calendarId=calendar_id, eventId=id).execute()
    print(a)

def create_event(summary,calendar_id,start,end,location):
    body = {
        'summary': summary,
        'description': 'A chance to hear more about Google\'s developer products.',
        'location': location,
        'start': {
            'dateTime': change_to_web(str(start)),
            'timeZone': 'Europe/Prague',
        },
        'end': {
            'dateTime': change_to_web(str(end)),
            'timeZone': 'Europe/Prague',
        },
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


def add_events_to_db(id):
    #pouzi to iste ako si to robil na webhooku teda dataweb a len funkciu na pridanie do db
    print('list')


def change_to_db(data):
    data = data.split("+")
    return data[0]

def change_to_web(data):
    data = data.split(" ")
    data = data[0]+'T'+data[1]
    return data


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

def change_to_dict_web(dataweb,name):
    webdict = []
    for i in range(len(dataweb['items'])):
        x = {}
        x['id'] = dataweb['items'][i]['id']
        try:
            x['name'] = dataweb['items'][i]['summary']
        except:
            x['name'] = 'None'
        x['end'] = datetime.datetime.strptime(change_to_db(dataweb['items'][i]['end']['dateTime']), '%Y-%m-%dT%H:%M:%S')
        x['start'] = datetime.datetime.strptime(change_to_db(dataweb['items'][i]['start']['dateTime']),
                                                   '%Y-%m-%dT%H:%M:%S')
        x['location'] = name
        webdict.append(x)
    return webdict


def change_to_dict_db(datadatabaza,name):
    if len(datadatabaza) == 0:
        return [{}]
    datadict = []
    for i in range(len(datadatabaza)):
        y = {}
        y['id'] = datadatabaza[i]['google_id']
        y['name'] = datadatabaza[i]['name']
        y['end'] = datadatabaza[i]['end']
        y['start'] = datadatabaza[i]['start']
        y['location'] = name
        datadict.append(y)
    return  datadict

def add_differnet_events_to_db(data,holder):
    calendar_id = holder['id']
    room_id = room_dao.get_all_id_by_name(data['location'])[0]['id']
    name =  data['name']
    start = data['start']
    end = data['end']
    google_id = data['id']
    tenant_id = holder['tenant_id']
    event_dao.add(calendar_id, room_id, name, start, end, google_id, tenant_id)

def add_differnet_events_to_web(data,holder):
    for i in range(len(holder)):
        calendar_id_id = holder[i]['id']
        calendar_id = holder[i]['google_id']
        room_id = room_dao.get_all_id_by_name(data['location'])[0]['id']
        location = data['location']
        name =  data['name']
        start = data['start']
        end = data['end']
        tenant_id = holder[i]['tenant_id']
        try:
            data_from_created = create_event(name,calendar_id,start,end,location)
        except:
            print('error na calendar_id pridavanie do ostatnych kalendarov')
            continue
        try:
            event_dao.add(calendar_id_id, room_id, name, start, end,data_from_created['id'], tenant_id)
        except:
            print('Error pri pridavani do db v add sync')
            continue

def delete_different_events_from_db(data):
    holder = event_dao.get_all_events_by_name_and_google_id(data['id'],data['name'])
    for i in range(len(holder)):
        try:
            event_dao.delete(holder[i]['id'])
        except:
            print('Chyba pri delete z db')

def delete_different_events_from_web(data,id):
    holder = calendar_dao.get_all_id_by_name_exept_id(data['location'],id)
    for i in range(len(holder)):
        event_data = event_dao.get_all_events_by_name_and_date_are_not_google_id(data['start'],data['end'],data['name'],data['id'])
        try:
            event_dao.delete(event_data[i]['id'])
        except:
            print("ERROR V DELETE Z db")
        try:
            print("---------------------------------------------------")
            print(holder[i]['google_id'],event_data[i]['google_id'])
            delete_event(holder[i]['google_id'],event_data[i]['google_id'])
        except:
            print("ERROR V DELETE Z WEBU")


# print_notification(" ")
# get_new_events(('3cmm3tsjhi70hgvk1j9p67k5r0@group.calendar.google.com'))
#pprint(create_event('test','3cmm3tsjhi70hgvk1j9p67k5r0@group.calendar.google.com'))
#pprint(get_all_calendars())
# print(closehook('a7407511-832e-4c65-8f49-f11e198d8c7c','lGFADe716IaqF4NRWk785rkrF_c'))
#print(createhook('2livateegthoron91afp2tg054@group.calendar.google.com'))
# pprint('halo')
#add_events_to_db('3cmm3tsjhi70hgvk1j9p67k5r0@group.calendar.google.com')
# insert_calendar('mrq1aii81hde7s2l5l5ogcti50@group.calendar.google.com')



