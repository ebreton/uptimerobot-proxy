from models import Event


def trigger_event(json_data):
    return Event(
        json_data.get('monitorFriendlyName'),
        json_data.get('alertType'),
        json_data.get('alertTypeFriendlyName'),
        json_data.get('alertDetails'),
        json_data.get('alertDuration'),
    )
