from models import Event


def trigger_event(data):
    return Event(
        data.get('monitorFriendlyName'),
        data.get('alertType'),
        data.get('alertTypeFriendlyName'),
        data.get('alertDetails'),
        data.get('alertDuration'),
    )
