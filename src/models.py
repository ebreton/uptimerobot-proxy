from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from entities import Event

db = SQLAlchemy()


class DBEvent(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    monitor_name = db.Column(db.String(80))
    alert_type = db.Column(db.Integer)
    alert_name = db.Column(db.String(10))
    alert_details = db.Column(db.String(256))
    alert_duration = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __init__(self, monitor_name, alert_type, alert_name, alert_details, alert_duration, timestamp=None):
        self.monitor_name = monitor_name
        self.alert_type = alert_type
        self.alert_name = alert_name
        self.alert_details = alert_details
        self.alert_duration = alert_duration
        self.timestamp = timestamp or datetime.now()

    @classmethod
    def from_event(cls, event):
        return cls(
            event.monitor_name,
            event.alert_type,
            event.alert_name,
            event.alert_details,
            event.alert_duration.seconds,
            timestamp=event.timestamp
        )


class DBStore:

    def __init__(self):
        self.db = db

    def init_db(self):
        self.db.create_all()
        DBEvent.query.delete()

    def init_app(self, app):
        self.db.init_app(app)

    def select(self):
        events = DBEvent.query.all()
        events.reverse()
        return events

    def flush(self, size):
        count = len(self)
        if count <= size:
            return
        # FIXME make a bulk delete here
        for event in DBEvent.query.limit(len(self)-size).all():
            db.session.delete(event)
        db.session.commit()

    def insert(self, event):
        db_event = DBEvent.from_event(event)
        self.db.session.add(db_event)
        self.db.session.commit()
        return db_event

    def create(self, data):
        return self.insert(Event.create_event(data))

    def __repr__(self):
        return f"<DBStore with {len(self)} events>"

    def __len__(self):
        return DBEvent.query.count()


storage = DBStore()
