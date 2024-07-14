import os
import pytest
from database import Database


@pytest.fixture(scope='session')
def db():
    db_path = 'tests.db'
    db = Database(db_path)

    yield db

    db.close()
    if os.path.exists(db_path):
        # Usuń plik bazy danych
        os.remove(db_path)
        print(f"Baza danych '{db_path}' została usunięta.")
    else:
        print(f"Baza danych '{db_path}' nie istnieje.")
