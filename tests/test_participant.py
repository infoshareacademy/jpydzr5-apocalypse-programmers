import pendulum
import pytest
from classes import *
from decimal import Decimal


@pytest.fixture
def participant(db):
    participant = Participant("participant@example.com", "password123")
    participant.save()
    return participant


def test_participant_creation(participant):
    assert participant.person_id is not None


def test_participant_buy_ticket(participant):
    show = Show(1, pendulum.now('Europe/Warsaw'), pendulum.now('Europe/Warsaw'), Decimal('99.99'))
    show.save()
    ticket = participant.buy_ticket(show)
    assert ticket.ticket_id is not None
    assert ticket.participant_id == participant.person_id
