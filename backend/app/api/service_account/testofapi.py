import os
from pprint import pprint

from service_account import get_service, get_other_service



API_NAME='calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']
location  = os.path.dirname(os.path.abspath(__file__)) +'\coworkreservation-213a4920386a.json'
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


# pprint(insert_calendar('3cmm3tsjhi70hgvk1j9p67k5r0@group.calendar.google.com'))
pprint(get_all_calendars())
# pprint('halo')


