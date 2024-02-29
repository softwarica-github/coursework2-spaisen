import sqlite3

# Connect to the database
conn = sqlite3.connect('website_blocker.db')
cursor = conn.cursor()

# Get the list of tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# List the content of each table
for table in tables:
    table_name = table[0]
    print(f"\nContent of table '{table_name}':")
    
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)

# Close the connection
conn.close()
