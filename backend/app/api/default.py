from flask.blueprints import Blueprint
from flask import render_template,request
from flask_swagger_ui import get_swaggerui_blueprint
from flask.helpers import send_from_directory
from app.api.service_account.service_account import *

from app.daos import event_dao,room_dao


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
    count_of_events_in_db, google_id, all_events = event_dao.get_all_events_from_calendar_resource_id_with_count("IByHQiFjwaCWNSe6F-q8PpUZ6mU","c8a721c9-72af-472e-ad7d-7a9e9e15f3f0")

    print(room_dao.check_if_exist("IByHQiFjwaCWNSe6F-q8PpUZ6mU","c8a721c9-72af-472e-ad7d-7a9e9e15f3f0"))
    return render_template("base.html")

def close_resource():
    closehook('3cmm3tsjhi70hgvk1j9p67k5r0@group.calendar.google.com',"wefsdf")
    return render_template("base.html")


@default_bp.route("/tests", methods=["POST","GET"])
def get_notifications():
    notifications = request.headers['X-Goog-Resource-ID']
    id_webhook = request.headers['X-Goog-Channel-ID']
    resourceid = request.headers['X-Goog-Resource-ID']

    if room_dao.check_if_exist(resourceid,id_webhook) == False:
        print("NO SUCH VALUES IN DB")
        print_notification(notifications)
        return render_template("base.html")


    count_of_events_in_db,google_id,all_events = event_dao.get_all_events_from_calendar_resource_id_with_count[resourceid,id_webhook]



    if count_of_events_in_db == 0 or google_id == None or all_events == {}:
        print("NO SUCH VALUES IN DB")
        print_notification(notifications)
        return render_template("base.html")


    try:
        data = get_all_events(google_id)
        count = len(data['items'])
    except:
        return render_template("base.html")

    web_data = change_to_dict_web(data)
    db_data  = change_to_dict_db(all_events)

    get_all_events_that_are_not_in_db = [i for i in web_data if i not in db_data]  # pomocou tohto viem najst nove

    for i in range(len(get_all_events_that_are_not_in_db)):
        #pridanie do db a na web, prve treba aby boli pridane do db a potom az naweb
        print(get_all_events_that_are_not_in_db[i])

    get_all_events_that_are_not_in_web = [i for i in db_data if i not in web_data]

    for i in range(len(get_all_events_that_are_not_in_web)):
        # vymazanie z db a z web, prve treba aby boli vymazane z db a potom az web
        print(get_all_events_that_are_not_in_db[i])

    print_notification(notifications)

    # if count_of_events_in_db == count :
    #     print(request.headers['X-Goog-Channel-ID']) #c8a721c9-72af-472e-ad7d-7a9e9e15f3f0
    #     print(request.headers['X-Goog-Message-Number']) #81219982
    #     print(request.headers['X-Goog-Resource-ID']) #IByHQiFjwaCWNSe6F-q8PpUZ6mU
    #     print(request.headers['X-Goog-Resource-State'])
    #     print("NOTIFICATION:")
    #     print_notification(notifications)

    return render_template("base.html")