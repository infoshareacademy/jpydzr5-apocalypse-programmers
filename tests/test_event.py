import pytest
from classes import *


@pytest.fixture
def event(db):
    event = Event("Test Event", "Conference", 1)
    event.save()
    return event


def test_event_creation(event):
    assert event.event_id is not None


def test_event_retrieval(event):
    retrieved_event = Event.get_by_id(event.event_id)
    assert retrieved_event is not None
    assert retrieved_event.name == "Test Event"
    assert retrieved_event.event_type == "Conference"
    assert retrieved_event.creator_id == 1


def test_event_update(event):
    event.name = "Updated Event"
    event.save()
    updated_event = Event.get_by_id(event.event_id)
    assert updated_event.name == "Updated Event"


def test_event_deletion(event):
    event_id = event.event_id
    event.delete()
    deleted_event = Event.get_by_id(event_id)
    assert deleted_event is None
