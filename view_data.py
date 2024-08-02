import sqlite3

# Connect to the database
conn = sqlite3.connect('predictions.db')
cursor = conn.cursor()

# Query the data
cursor.execute('SELECT * FROM predictions')
rows = cursor.fetchall()

# Print the data
for row in rows:
    print(row)

# Close the connection
conn.close()
