import sqlite3
import pendulum


class Database:
    def __init__(self, db_name="shop.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS person (
                    id INTEGER PRIMARY KEY,
                    email TEXT,
                    password TEXT,
                    first_name TEXT,
                    last_name TEXT
                )
                ''')

            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS event (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    event_type TEXT,
                    creator_id INTEGER,
                    FOREIGN KEY (creator_id) REFERENCES person(id)
                )
                ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS show (
                    id INTEGER PRIMARY KEY,
                    event_id INTEGER,
                    name TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    price NUMERIC,
                    FOREIGN KEY (event_id) REFERENCES event(id)
                )
                ''')

            self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS ticket (
                        id INTEGER PRIMARY KEY,
                        participant_id INTEGER,
                        show_id INTEGER,
                        FOREIGN KEY (participant_id) REFERENCES person(id),
                        FOREIGN KEY (show_id) REFERENCES show(id)
                    )
                    ''')

    def add_person(self, email: str, password: str) -> int:
        with self.conn:
            cursor = self.conn.execute('''
                INSERT INTO person (email, password) VALUES (?, ?)
                ''', (email, password))
            return cursor.lastrowid

    def update_person(self, person_id, email, password):
        with self.conn:
            self.conn.execute('''
                        UPDATE person
                        SET email = ?, password = ?
                        WHERE id = ?
                    ''', (email, password, person_id))

    def get_person_by_id(self, person_id):
        cursor = self.conn.execute("SELECT id, email, password FROM person WHERE id = ?", (person_id,))
        return cursor.fetchone()

    def delete_person(self, person_id):
        self.conn.execute("DELETE FROM person WHERE id = ?", (person_id,))

    def login_person(self, email, password):
        cursor = self.conn.execute(
            "SELECT id, email, password FROM person WHERE email = ? AND password = ?",
            (email, password,)
        )
        return cursor.fetchone()

    def create_show(self, event_id, name, start_time, end_time, price) -> int:
        with self.conn:
            cursor = self.conn.execute('''
                 INSERT INTO show (event_id, name, start_time, end_time, price)
                 VALUES (?, ?, ?, ?, ?)
                 ''', (
                event_id,
                str(name),
                start_time.to_iso8601_string(),
                end_time.to_iso8601_string(),
                str(price)
            ))
            return cursor.lastrowid

    def update_show(self, show_id, name, start_time, end_time, price):
        with self.conn:
            self.conn.execute('''
                        UPDATE show
                        SET name = ?, start_time = ?, end_time = ?, price = ?
                        WHERE id = ?
                    ''', (
                str(name),
                start_time.to_iso8601_string(),
                end_time.to_iso8601_string(),
                str(price),
                show_id
            ))

    def get_show_by_id(self, show_id):
        cursor = self.conn.execute("SELECT id, event_id, name, start_time, end_time, price FROM show WHERE id = ?", (show_id,))
        row = cursor.fetchone()

        if row:
            return row[0], row[1], row[2], pendulum.parse(row[3]), pendulum.parse(row[4]), row[5]
        return None

    def get_shows_by_event_id(self, event_id):
        cursor = self.conn.execute("SELECT id FROM show WHERE event_id = ?", (event_id,))
        return cursor.fetchall()

    def get_shows_with_enough_tickets(self, event_id, requested_tickets):
        # TODO: dodać filtr wystarczającej liczbę biletów
        cursor = self.conn.execute("SELECT id FROM show WHERE event_id = ?", (event_id,))
        return cursor.fetchall()



    def delete_show(self, show_id):
        self.conn.execute("DELETE FROM show WHERE id = ?", (show_id,))

    def add_ticket(self, show_id, participant_id) -> int:
        with self.conn:
            cursor = self.conn.execute('''
                INSERT INTO ticket(show_id, participant_id)
                VALUES(?, ?)
                ''', (
                show_id,
                participant_id
            ))
            return cursor.lastrowid

    def update_ticket(self, ticket_id, participant_id):
        with self.conn:
            self.conn.execute('''
                        UPDATE ticket
                        SET participant_id = ?
                        WHERE id = ?
                    ''', (participant_id, ticket_id,))

    def get_ticket_by_id(self, ticket_id):
        cursor = self.conn.execute("SELECT id, show_id, participant_id FROM ticket WHERE id = ?", (ticket_id,))
        return cursor.fetchone()

    def delete_ticket(self, ticket_id):
        self.conn.execute("DELETE FROM ticket WHERE id = ?", (ticket_id,))

    def create_event(self, name, event_type, creator_id) -> int:
        with self.conn:
            cursor = self.conn.execute('''
                INSERT INTO event (name, event_type, creator_id) VALUES (?, ?, ?)
                ''', (name, event_type, creator_id))
            return cursor.lastrowid

    def update_event(self, event_id, name, event_type):
        with self.conn:
            self.conn.execute('''
                        UPDATE event
                        SET name = ?, event_type = ?
                        WHERE id = ?
                    ''', (name, event_type, event_id))

    def get_tickets(self, participant_id):
        cursor = self.conn.execute("""
            SELECT ticket.id, event_id, show_id
            FROM ticket
              INNER JOIN show
                ON ticket.show_id=show.id
            WHERE participant_id = ?""",
                                   (participant_id,))
        return cursor.fetchall()

    def get_event_by_id(self, event_id):
        cursor = self.conn.execute("SELECT id, name, event_type, creator_id  FROM event WHERE id = ?", (event_id,))
        return cursor.fetchone()

    def get_events_by_creator_id(self, creator_id):
        cursor = self.conn.execute("SELECT id FROM event WHERE creator_id = ?", (creator_id,))
        return cursor.fetchall()

    def get_available_events(self):
        # TODO: dodać filtr, żeby wydarzenia które już były lub które nie mają wolnych biletów się nie wyświetlały
        cursor = self.conn.execute("SELECT id FROM event")
        return cursor.fetchall()


    def delete_event(self, event_id):
        self.conn.execute("DELETE FROM event WHERE id = ?", (event_id,))

    def close(self):
        self.conn.close()