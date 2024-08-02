# init_db.py
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    flight_distance INTEGER,
    inflight_entertainment INTEGER,
    baggage_handling INTEGER,
    cleanliness INTEGER,
    departure_delay INTEGER,
    arrival_delay INTEGER,
    gender INTEGER,
    customer_type INTEGER,
    travel_type INTEGER,
    class_type INTEGER,
    prediction TEXT
)
''')

conn.commit()
conn.close()
