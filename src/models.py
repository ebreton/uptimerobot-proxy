from flask_sqlalchemy import SQLAlchemy

from entities import Event

db = SQLAlchemy()


class DBEvent(db.Model, Event):

    id = db.Column(db.Integer, primary_key=True)
    monitor_name = db.Column(db.String(80))
    alert_type = db.Column(db.Integer)
    alert_name = db.Column(db.String(10))
    alert_details = db.Column(db.String(256))
    alert_duration = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __init__(self, monitor_name, alert_type, alert_name, alert_details, alert_duration, timestamp=None):
        Event.__init__(
            self,
            monitor_name,
            alert_type,
            alert_name,
            alert_details,
            alert_duration,
            timestamp=timestamp
        )

    def __repr__(self):
        return Event.__repr__(self)

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


class DBStore:

    def __init__(self):
        self.db = db

    def init_db(self):
        self.db.create_all()
        DBEvent.query.delete()

    def init_app(self, app):
        self.db.init_app(app)

    def get(self, event_id):
        return DBEvent.query.get(event_id)

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

    def create(self, event):
        if not isinstance(event, Event):
            event = Event.create_event(event)
        db_event = DBEvent.from_event(event)
        self.db.session.add(db_event)
        self.db.session.commit()
        return db_event

    def __repr__(self):
        return f"<DBStore with {len(self)} events>"

    def __len__(self):
        return DBEvent.query.count()


storage = DBStore()
