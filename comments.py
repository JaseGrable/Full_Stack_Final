import sqlite3

# Create the database and table
conn = sqlite3.connect('comments.db')
cursor = conn.cursor()

# Create the comments table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
''')

conn.commit()
conn.close()

print("Database and table created successfully.")
