import pytest
from database import Database


@pytest.fixture(scope='session')
def db():
    db = Database('tests.db')

    yield db

    db.close()