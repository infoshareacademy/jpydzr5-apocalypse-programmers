import pytest
from classes import *
import pendulum
from decimal import Decimal


@pytest.fixture
def show(db):
    start_time = pendulum.now('Europe/Warsaw')
    end_time = pendulum.now('Europe/Warsaw')
    show = Show(1, start_time, end_time, Decimal('99.99'))
    show.save()
    return show


def test_show_creation(show):
    assert show.show_id is not None


def test_show_retrieval(show):
    retrieved_show = Show.get_by_id(show.show_id)
    assert retrieved_show is not None
    assert retrieved_show.event_id == 1


def test_show_update(show):
    new_end_time = pendulum.now('Europe/Warsaw')
    show.end_time = new_end_time
    show.save()
    updated_show = Show.get_by_id(show.show_id)
    assert updated_show.end_time == new_end_time.to_iso8601_string()


def test_show_deletion(show):
    show_id = show.show_id
    show.delete()
    deleted_show = Show.get_by_id(show_id)
    assert deleted_show is None
