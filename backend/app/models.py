from flask_sqlalchemy.model import DefaultMeta
from app import db

BaseModel: DefaultMeta = db.Model


class Calendar(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    google_id = db.Column(db.String(255), nullable=False)
    resource_id = db.Column(db.String(255))
    webhook_id = db.Column(db.String(255))
    expiration = db.Column(db.String(255))

    events = db.relationship("Event", backref="calendar")


class Tenant(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    calendars = db.relationship("Calendar", backref="tenant")
    events = db.relationship("Event", backref="tenant")


class Event(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    calendar_id = db.Column(db.Integer, db.ForeignKey("calendar.id"))
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    start = db.Column(db.DateTime(timezone= True), nullable=False)
    end = db.Column(db.DateTime(timezone= True), nullable=False)
    google_id = db.Column(db.String(255), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id"))



class Room(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    equipment = db.Column(db.String(255))
    building = db.Column(db.String(255), nullable=False)
    room_number = db.Column(db.Integer, nullable=False)

    events = db.relationship("Event", backref="room")
