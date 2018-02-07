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
        self.alert_type = int(alert_type)
        self.alert_name = alert_name
        self.alert_details = alert_details
        self.alert_duration = alert_duration and int(alert_duration) or 0
        self.timestamp = timestamp or datetime.now()

    def __repr__(self):
        duration = timedelta(seconds=self.alert_duration)
        return f"<{self.__class__.__name__} for {self.monitor_name}: " \
            f"{self.alert_name}({self.alert_type}) since {str(duration)}, {self.alert_details}>"

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

    def _index(self):
        # use index to emulate ids
        for index, event in enumerate(self.store):
            event.id = index

    def init_db(self):
        pass

    def init_app(self, app):
        pass

    def get(self, event_id):
        return self.store[event_id]

    def select(self):
        self._index()
        return self.store

    def flush(self, size):
        self.store = deque(islice(self.store, 0, size))
        self._index()

    def create(self, event):
        if not isinstance(event, Event):
            event = Event.create_event(event)
        self.store.appendleft(event)
        self._index()
        return event

    def __repr__(self):
        return f"<Store with {len(self.store)} events>"

    def __len__(self):
        return len(self.store)


storage = Store()
