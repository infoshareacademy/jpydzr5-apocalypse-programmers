import pytest
from classes import *
from database import Database


@pytest.fixture
def event(db):
    return Event(db, "Test Event", "Conference", 1)


def test_event_creation(event):
    assert event.event_id is not None


def test_event_retrieval(db, event):
    retrieved_event = Event.get_by_id(db, event.event_id)
    assert retrieved_event is not None
    assert retrieved_event.name == "Test Event"
    assert retrieved_event.event_type == "Conference"
    assert retrieved_event.creator_id == 1


def test_event_update(db, event):
    event.name = "Updated Event"
    updated_event = Event.get_by_id(db, event.event_id)
    assert updated_event.name == "Updated Event"


def test_event_deletion(db, event):
    event_id = event.event_id
    event.delete()
    deleted_event = Event.get_by_id(db, event_id)
    assert deleted_event is None
