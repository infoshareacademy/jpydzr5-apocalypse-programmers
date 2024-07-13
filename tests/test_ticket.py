import pytest
from classes import *


@pytest.fixture
def ticket(db):
    return Ticket(db, 1, 1)


def test_ticket_creation(ticket):
    assert ticket.ticket_id is not None


def test_ticket_retrieval(db, ticket):
    retrieved_ticket = Ticket.get_by_id(db, ticket.ticket_id)
    assert retrieved_ticket is not None
    assert retrieved_ticket.show_id == 1
    assert retrieved_ticket.participant_id == 1


def test_ticket_deletion(db, ticket):
    ticket_id = ticket.ticket_id
    ticket.delete()
    deleted_ticket = Ticket.get_by_id(db, ticket_id)
    assert deleted_ticket is None
