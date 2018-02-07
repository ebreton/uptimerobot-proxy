"""
    Wraps data sent from uptimerobot into python objects. Following vars can be passed:
      - monitorID: the ID of the monitor
      - monitorURL: the URL of the monitor
      - monitorFriendlyName: the friendly name of the monitor
      - alertType: 1: down, 2: up, 3: SSL expiry notification
      - alertTypeFriendlyName: Down or Up
      - alertDetails: any info regarding the alert -if exists-
      - alertDuration: in seconds and only for up events
      - monitorAlertContacts: the alert contacts associated with the alert in the format of
            457;2;john@doe.com - alertContactID;alertContactType, alertContactValue
      - sslExpiryDate: only for SSL expiry notifications
      - sslExpiryDaysLeft: only for SSL expiry notifications
"""
from datetime import datetime, timedelta
from collections import deque
from itertools import islice


class Event:

    def __init__(self, monitor_name, alert_type, alert_name, alert_details, alert_duration, timestamp=None):
        self.monitor_name = monitor_name
        self.alert_type = alert_type
        self.alert_name = alert_name
        self.alert_details = alert_details
        seconds = alert_duration and int(alert_duration) or 0
        self.alert_duration = timedelta(seconds=seconds)
        self.timestamp = timestamp or datetime.now()

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.alert_type}) for " \
            f"{self.monitor_name}: {self.alert_name} since {str(self.alert_duration)}>"

    @classmethod
    def create_event(cls, data):
        return cls(
            data.get('monitorFriendlyName'),
            data.get('alertType'),
            data.get('alertTypeFriendlyName'),
            data.get('alertDetails'),
            data.get('alertDuration'),
        )


class Store:

    def __init__(self):
        self.store = deque()

    def init_db(self):
        pass

    def init_app(self, app):
        pass

    def select(self):
        return self.store

    def flush(self, size):
        self.store = deque(islice(self.store, 0, size))

    def insert(self, item):
        self.store.appendleft(item)

    def create(self, data):
        event = Event.create_event(data)
        self.insert(event)
        return event

    def __repr__(self):
        return f"<Store with {len(self.store)} events>"

    def __len__(self):
        return len(self.store)


storage = Store()
