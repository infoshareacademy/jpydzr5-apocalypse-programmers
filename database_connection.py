import sqlite3


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._conn = sqlite3.connect('ticket_system.db')
            cursor = cls._instance._conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS person (
                    id INTEGER PRIMARY KEY,
                    email TEXT,
                    password TEXT,
                    first_name TEXT,
                    last_name TEXT
                )
                ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS event (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    event_type TEXT,
                    creator_id INTEGER,
                    FOREIGN KEY (creator_id) REFERENCES person(id)
                )
                ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS show (
                    id INTEGER PRIMARY KEY,
                    event_id INTEGER,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    price NUMERIC,
                    FOREIGN KEY (event_id) REFERENCES event(id)
                )
                ''')

            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ticket (
                        id INTEGER PRIMARY KEY,
                        participant_id INTEGER,
                        show_id INTEGER,
                        FOREIGN KEY (participant_id) REFERENCES person(id),
                        FOREIGN KEY (show_id) REFERENCES show(id)
                    )
                    ''')

            cls._instance._conn.commit()

        return cls._instance

    def get_connection(self):
        return self._instance._conn
