import pendulum
import pytest
from classes import *
from decimal import Decimal


@pytest.fixture
def participant(db):
    participant = Participant(db, "participant@example.com", "password123")
    return participant


def test_participant_creation(participant):
    assert participant.person_id is not None


def test_participant_buy_ticket(db, participant):
    show = Show(db, 1, 'test name', pendulum.now('Europe/Warsaw'), pendulum.now('Europe/Warsaw'), Decimal('99.99'))
    ticket = participant.buy_ticket(show)
    assert ticket.ticket_id is not None
    assert ticket.participant_id == participant.person_id
