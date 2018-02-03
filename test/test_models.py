from models import Store


def test_store():
    storage = Store()
    assert repr(storage) == '<Store with 0 events>'
    storage.store.append(1)
    assert repr(storage) == '<Store with 1 events>'
    storage.flush(0)
    assert repr(storage) == '<Store with 0 events>'
