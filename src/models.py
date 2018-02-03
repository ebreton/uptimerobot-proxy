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


class Event:

    def __init__(self, monitor_name, alert_type, alert_name, alert_details, alert_duration):
        self.monitor_name = monitor_name
        self.alert_type = alert_type
        self.alert_name = alert_name
        self.alert_details = alert_details
        self.alert_duration = alert_duration

    def __repr__(self):
        return "<Event for {0.monitor_name}: {0.alert_name} ({0.alert_type}) since {0.alert_duration}>".format(self)
