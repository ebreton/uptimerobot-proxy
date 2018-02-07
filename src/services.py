import json

from datetime import timedelta

from settings import UPTIMEROBOT_DOWN, UPTIMEROBOT_UP, \
    E2EMONITORING_DOWN, E2EMONITORING_UP, E2EMONITORING_SERVICE


class Proxy:

    def event_to_json(self, event):
        # prepare information when site goes DOWN
        if event.alert_type == UPTIMEROBOT_DOWN:
            priority = E2EMONITORING_DOWN
            description = f"{event.monitor_name} is {event.alert_name}: {event.alert_details}."
        # prepare information when back UP
        elif event.alert_type == UPTIMEROBOT_UP:
            priority = E2EMONITORING_UP
            duration = timedelta(seconds=event.alert_duration)
            description = f"{event.monitor_name} is {event.alert_name} ({event.alert_details}). " \
                f"It was down for {duration}."
        # other alerts are not supported
        else:
            raise NotImplementedError(f"Alert not supported [{event.alert_type}: {event.alert_name}]")
        # return a JSON compliant to E2E monitoring expectations
        return json.dumps({
            "u_business_service": E2EMONITORING_SERVICE,
            "u_priority": priority,
            "u_short_description": f"{event.monitor_name} is {event.alert_name}",
            "u_description": description,
            }, sort_keys=True, indent=2)
