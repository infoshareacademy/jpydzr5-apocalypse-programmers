import sqlite3


class DatabaseConnection:
    _instances = {}

    def __new__(cls, db_filename='ticket_system.db'):
        if db_filename not in cls._instances:
            instance = super(DatabaseConnection, cls).__new__(cls)
            instance._conn = sqlite3.connect(db_filename)
            cursor = instance._conn.cursor()

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

            instance._conn.commit()
            cls._instances[db_filename] = instance

        return cls._instances[db_filename]

    def get_connection(self):
        return self._conn

