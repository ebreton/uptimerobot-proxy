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
import json

from datetime import datetime, timedelta
from collections import deque
from itertools import islice

from settings import UPTIMEROBOT_DOWN, UPTIMEROBOT_UP, \
    E2EMONITORING_DOWN, E2EMONITORING_UP, E2EMONITORING_SERVICE


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

    def to_json(self):
        # prepare information when site goes DOWN
        if self.alert_type == UPTIMEROBOT_DOWN:
            priority = E2EMONITORING_DOWN
            description = f"{self.monitor_name} is {self.alert_name}: {self.alert_details}."
        # prepare information when back UP
        elif self.alert_type == UPTIMEROBOT_UP:
            priority = E2EMONITORING_UP
            description = f"{self.monitor_name} is {self.alert_name} ({self.alert_details}). " \
                f"It was down for {self.alert_duration}."
        # other alerts are not supported
        else:
            raise NotImplementedError(f"Alert not supported [{self.alert_type}: {self.alert_name}]")
        # return a JSON compliant to E2E monitoring expectations
        return json.dumps({
            "u_business_service": E2EMONITORING_SERVICE,
            "u_priority": priority,
            "u_short_description": f"{self.monitor_name} is {self.alert_name}",
            "u_description": description,
        })

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
