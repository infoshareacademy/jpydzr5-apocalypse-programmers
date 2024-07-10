import pytest
from classes import *
from database_connection import DatabaseConnection


@pytest.fixture
def ticket(db):
    ticket = Ticket(1, 1)
    ticket.save()
    return ticket

def test_ticket_creation(ticket):
    assert ticket.ticket_id is not None

def test_ticket_retrieval(ticket):
    retrieved_ticket = Ticket.get_by_id(ticket.ticket_id)
    assert retrieved_ticket is not None
    assert retrieved_ticket.show_id == 1
    assert retrieved_ticket.participant_id == 1

def test_ticket_deletion(ticket):
    ticket_id = ticket.ticket_id
    ticket.delete()
    deleted_ticket = Ticket.get_by_id(ticket_id)
    assert deleted_ticket is None