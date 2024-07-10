import pytest
from classes import *
from database_connection import DatabaseConnection


@pytest.fixture
def participant(db):
    participant = Participant("participant@example.com", "password123")
    participant.save()
    return participant


def test_participant_creation(participant):
    assert participant.person_id is not None


def test_participant_buy_ticket(participant):
    from classes import Show
    from datetime import datetime
    from decimal import Decimal

    show = Show(1, datetime.now(), datetime.now(), Decimal('99.99'))
    show.save()
    ticket = participant.buy_ticket(show)
    assert ticket.ticket_id is not None
    assert ticket.participant_id == participant.person_id
