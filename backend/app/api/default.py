from flask.blueprints import Blueprint
from flask import render_template,request
from flask_swagger_ui import get_swaggerui_blueprint
from flask.helpers import send_from_directory
from app.api.service_account.service_account import *
from app.daos import event_dao,calendar_dao


### swagger specific ###
swagger_url = "/swagger"
api_url = "/static/swagger.json"
swagger_bp = get_swaggerui_blueprint(
    swagger_url, api_url, config={"app_name": "Cowork-Reservation"}
)

default_bp = Blueprint("default_bp", __name__)


@default_bp.route("/", methods=["GET"])
def get_site():
    # TODO: Replace with correct html file
    return render_template("base.html")


@default_bp.route("/admin", methods=["GET"])
def get_admin_site():
    # TODO: Replace with correct html file
    return render_template("base.html")


@default_bp.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@default_bp.route("/resources", methods=["GET"])
def get_resources():


    print('hello')
    # start = datetime.datetime.strptime(change_to_db('2022-1-17T12:30:00+01:00'), '%Y-%m-%dT%H:%M:%S')
    # end = datetime.datetime.strptime(change_to_db('2022-1-17T19:30:00+01:00'), '%Y-%m-%dT%H:%M:%S')
    # print(create_event('Test','2livateegthoron91afp2tg054@group.calendar.google.com', change_to_web(str(start)),change_to_web(str(end))))

    id_webhook = 'c8a721c9-72af-472e-ad7d-7a9e9e15f3f0'
    resourceid = 'IByHQiFjwaCWNSe6F-q8PpUZ6mU'

    all_events = event_dao.get_all_events_from_calendar_resource_id(resourceid, id_webhook)
    calendar_id_in_db,name,google_id = calendar_dao.get_all_calendar_by_resource_and_webhook_id(resourceid, id_webhook)


    try:
        data = get_all_events(google_id)
    except:
        print("chyba na web get")
        return render_template("base.html")

    web_data = change_to_dict_web(data, name)
    db_data = change_to_dict_db(all_events, name)



    get_all_events_that_are_not_in_db = [i for i in web_data if i not in db_data]  # pomocou tohto viem najst nove


    if len(get_all_events_that_are_not_in_db) != 0:
        get_data_for_db = calendar_dao.get_one(calendar_id_in_db)
        get_data_for_web = calendar_dao.get_all_id_by_name_exept_id(get_all_events_that_are_not_in_db[0]['location'], calendar_id_in_db)
    else:
        get_data_for_db = None
        get_data_for_web = None


    for i in range(len(get_all_events_that_are_not_in_db)):
        # pridanie do db a na web, prve treba aby boli pridane do db a potom az naweb
        add_differnet_events_to_db(get_all_events_that_are_not_in_db[i],get_data_for_db)
        add_differnet_events_to_web(get_all_events_that_are_not_in_db[i],get_data_for_web)



    #to do error pri delete nechce to deletovat veci z db a z internetu ciastocne davaj pozor
    print(web_data)
    print(db_data)

    get_all_events_that_are_not_in_web = [i for i in db_data if i not in web_data]
    print("-------------------------------------------")
    print(get_all_events_that_are_not_in_web)

    print("-------------------------------------------")


    if get_all_events_that_are_not_in_web == [{}]:
        return  render_template("base.html")


    for i in range(len(get_all_events_that_are_not_in_web)):
        delete_different_events_from_db(get_all_events_that_are_not_in_web[i])
        delete_different_events_from_web(get_all_events_that_are_not_in_web[i],calendar_id_in_db)
        # vymazanie z db a z web, prve treba aby boli vymazane z db a potom az web

    return render_template("base.html")

def close_resource():
    closehook('3cmm3tsjhi70hgvk1j9p67k5r0@group.calendar.google.com',"wefsdf")
    return render_template("base.html")


@default_bp.route("/tests", methods=["POST","GET"])
def get_notifications():
    return render_template("base.html")

    notifications = request.headers['X-Goog-Resource-ID']
    id_webhook = request.headers['X-Goog-Channel-ID']
    resourceid = request.headers['X-Goog-Resource-ID']


    check = calendar_dao.check_if_exist(resourceid,id_webhook)
    if check == False:
        print("NO SUCH VALUES IN DB FIRST TRIGGER ")
        print_notification(notifications)
        return render_template("base.html")

    all_events = event_dao.get_all_events_from_calendar_resource_id(resourceid, id_webhook)
    calendar_id_in_db, name, google_id = calendar_dao.get_all_calendar_by_resource_and_webhook_id(resourceid,
                                                                                                  id_webhook)

    try:
        data = get_all_events(google_id)
    except:
        print("chyba na web get")
        return render_template("base.html")

    web_data = change_to_dict_web(data, name)
    db_data = change_to_dict_db(all_events, name)

    get_all_events_that_are_not_in_db = [i for i in web_data if i not in db_data]  # pomocou tohto viem najst nove

    if len(get_all_events_that_are_not_in_db) != 0:
        get_data_for_db = calendar_dao.get_one(calendar_id_in_db)
        get_data_for_web = calendar_dao.get_all_id_by_name_exept_id(get_all_events_that_are_not_in_db[0]['location'],
                                                                    calendar_id_in_db)
    else:
        get_data_for_db = None
        get_data_for_web = None

    for i in range(len(get_all_events_that_are_not_in_db)):
        # pridanie do db a na web, prve treba aby boli pridane do db a potom az naweb
        add_differnet_events_to_db(get_all_events_that_are_not_in_db[i], get_data_for_db)
        add_differnet_events_to_web(get_all_events_that_are_not_in_db[i], get_data_for_web)

    # to do error pri delete nechce to deletovat veci z db a z internetu ciastocne davaj pozor

    get_all_events_that_are_not_in_web = [i for i in db_data if i not in web_data]


    if get_all_events_that_are_not_in_web == [{}]:
        return render_template("base.html")

    for i in range(len(get_all_events_that_are_not_in_web)):
        delete_different_events_from_db(get_all_events_that_are_not_in_web[i])
        delete_different_events_from_web(get_all_events_that_are_not_in_web[i], calendar_id_in_db)
        # vymazanie z db a z web, prve treba aby boli vymazane z db a potom az web

    print_notification(notifications)
    # if count_of_events_in_db == count :
    #     print(request.headers['X-Goog-Channel-ID']) #c8a721c9-72af-472e-ad7d-7a9e9e15f3f0
    #     print(request.headers['X-Goog-Message-Number']) #81219982
    #     print(request.headers['X-Goog-Resource-ID']) #IByHQiFjwaCWNSe6F-q8PpUZ6mU
    #     print(request.headers['X-Goog-Resource-State'])
    #     print("NOTIFICATION:")
    #     print_notification(notifications)

    return render_template("base.html")
