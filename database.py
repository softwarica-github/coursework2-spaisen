import sqlite3

# Connect to or create the database
conn = sqlite3.connect('website_blocker.db')
cursor = conn.cursor()

# Create Top 25 Social sites table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Top25SocialSites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_name TEXT NOT NULL
    )
''')

# Create Top 25 Work Sites table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Top25WorkSites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_name TEXT NOT NULL
    )
''')

# Create Top 25 Kids sites table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Top25KidsSites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_name TEXT NOT NULL
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()
