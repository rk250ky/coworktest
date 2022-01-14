from flask.blueprints import Blueprint
from flask import render_template,request
from flask_swagger_ui import get_swaggerui_blueprint
from flask.helpers import send_from_directory
from app.api.service_account.service_account import *
import sys

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
    createhook('3cmm3tsjhi70hgvk1j9p67k5r0@group.calendar.google.com')
    return render_template("base.html")

def close_resource():
    closehook('3cmm3tsjhi70hgvk1j9p67k5r0@group.calendar.google.com',"wefsdf")
    return render_template("base.html")


@default_bp.route("/test", methods=["POST","GET"])
def get_notifications():
    notifications = request.json
    sys.stderr.write(notifications)
    print("NOTIFICATION:")

    return render_template("base.html",notifications=notifications)