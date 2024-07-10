import pytest
from database_connection import DatabaseConnection

@pytest.fixture(scope='session')
def db():
    connection = DatabaseConnection()
    yield connection
    # Cleanup: Zamknięcie połączenia po testach
    connection.get_connection()