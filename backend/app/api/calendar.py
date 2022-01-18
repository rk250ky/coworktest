from flask import jsonify, request, make_response, render_template
from flask.blueprints import Blueprint
from app.daos import calendar_dao

calendar_bp = Blueprint("calendar_bp", __name__)


@calendar_bp.route("/calendars/", methods=["GET"])
def get_calendar_list():
    # TODO: check if tenant has permissions to view all calendars
    url_args = request.args
    filters = {}
    sort = []
    results_range = []
    for key, value in url_args.items(multi=True):
        if key == "id":
            if "id" in filters:
                filters["id"].append(int(value))
            else:
                filters["id"] = [int(value)]
        elif key == "_sort":
            sort.insert(0, str(value))
        elif key == "_order":
            sort.insert(1, str(value))
        elif key == "_start":
            results_range.insert(0, int(value))
        elif key == "_end":
            results_range.insert(1, int(value))
        else:
            if key in filters:
                filters[key].append(value)
            else:
                filters[key] = [value]
    results = calendar_dao.get_all(filters, sort, results_range)
    resp = make_response(jsonify(results["data"]), 200)
    resp.headers["Access-Control-Expose-Headers"] = "X-Total-Count"
    resp.headers["X-Total-Count"] = results["count"]
    return resp


@calendar_bp.route("/calendars/<id>", methods=["GET"])
def get_calendar(id):
    # TODO: check if tenant has permissions to view desired calendar
    return jsonify(calendar_dao.get_one(id))


@calendar_bp.route("/calendars/<id>", methods=["PUT"])
def update_calendar(id):
    # TODO: check if tenant has permissions to update desired calendar
    data = request.json
    return jsonify(calendar_dao.update(id, data))


@calendar_bp.route("/calendars/<id>", methods=["DELETE"])
def delete_calendar(id):
    # TODO: check if tenant has permissions to delete calendars
    calendar_dao.delete(id)
    return jsonify({})


@calendar_bp.route("/calendars/", methods=["POST"])
def create_calendar():
    # TODO: check if tenant has permissions to add calendars
    # try:
    data = request.json
    new_calendar = calendar_dao.add(
        int(data["tenant_id"]), data["name"], data["google_id"] , data["resource_id"], data["webhook_id"]
    )
    return jsonify(new_calendar)
    # except Exception as err:
