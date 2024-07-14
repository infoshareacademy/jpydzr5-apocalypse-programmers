import pytest
from classes import *

@pytest.fixture
def person(db):
    return Person(db,"test@example.com", "password123")


def test_person_creation(person):
    assert person.person_id is not None


def test_person_retrieval(db, person):
    retrieved_person = Person.get_by_id(db, person.person_id)
    assert retrieved_person is not None
    assert retrieved_person.email == "test@example.com"


def test_person_update(db, person):
    email = "new@example.com"
    password = "newpassword123"
    person.change_email(email)
    person.change_password(password)
    logged_person = person.login_person(db, email, password)
    assert person.person_id == logged_person.person_id


def test_person_deletion(db, person):
    person_id = person.person_id
    person.delete()
    deleted_person = Person.get_by_id(db, person_id)
    assert deleted_person is None
