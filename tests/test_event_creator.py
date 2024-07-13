import pytest
from classes import *
from database import Database


@pytest.fixture
def event_creator(db):
    event_creator = EventCreator(db, "creator@example.com", "password123")

    return event_creator


def test_event_creator_creation(event_creator):
    assert event_creator.person_id is not None


def test_event_creator_add_event(event_creator):
    event = event_creator.add_event("New Event", "Workshop")
    assert event.event_id is not None
    assert event.creator_id == event_creator.person_id


def test_event_creator_delete_event(db, event_creator):
    event = event_creator.add_event("Event to Delete", "Seminar")
    event_creator.del_event(event)
    assert Event.get_by_id(db, event.event_id) is None


def test_event_creator_rename_event(db, event_creator):
    event = event_creator.add_event("Event to Rename", "Lecture")
    event_creator.rename_event(event, "Renamed Event")
    assert Event.get_by_id(db, event.event_id).name == "Renamed Event"
