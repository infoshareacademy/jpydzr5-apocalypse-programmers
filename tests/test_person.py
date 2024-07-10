import pytest
from classes import *
from database_connection import DatabaseConnection

@pytest.fixture
def person(db):
    person = Person("test@example.com", "password123")
    person.save()
    return person

def test_person_creation(person):
    assert person.person_id is not None

def test_person_retrieval(person):
    retrieved_person = Person.get_by_id(person.person_id)
    assert retrieved_person is not None
    assert retrieved_person.email == "test@example.com"

def test_person_update(person):
    person.change_email("new@example.com")
    person.change_password("newpassword123")
    updated_person = Person.get_by_id(person.person_id)
    assert updated_person.email == "new@example.com"
    assert updated_person.match_pass("newpassword123")

def test_person_deletion(person):
    person_id = person.person_id
    person.delete()
    deleted_person = Person.get_by_id(person_id)
    assert deleted_person is None