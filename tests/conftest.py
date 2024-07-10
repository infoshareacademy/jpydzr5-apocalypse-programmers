import pytest
from database_connection import DatabaseConnection

@pytest.fixture(scope='session')
def db():
    connection = DatabaseConnection('tests.db')

    yield connection.get_connection()

    connection.get_connection().close()