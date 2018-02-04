from flask_sqlalchemy import SQLAlchemy

from models import Event

db = SQLAlchemy()


class DBEvent(db.Model, Event):

    id = db.Column(db.Integer, primary_key=True)
    monitor_name = db.Column(db.String(80))
    alert_type = db.Column(db.Integer)
    alert_name = db.Column(db.String(10))
    alert_details = db.Column(db.String(256))
    alert_duration = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    @classmethod
    def from_event(cls, event):
        return cls(
            event.monitor_name,
            event.alert_type,
            event.alert_name,
            event.alert_details,
            event.alert_duration,
            timestamp=event.timestamp
        )
