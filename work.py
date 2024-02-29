import sqlite3
import socket

# List of work-related websites
work_sites = [
    'slack.com',
    'trello.com',
    'teams.microsoft.com',
    'grammarly.com',
    'workspace.google.com',
    'zoom.us',
    'loom.com',
    'sharepoint.com',
    'nuclino.com',
    'guru.com',
    'miro.com',
    'figma.com',
    'whatfix.com',
    'proprofs.com',
    'trainual.com',
    'lessonly.com',
    'asana.com',
    'airtable.com',
    'confluence.atlassian.com',
    'clickup.com',
    'monday.com',
    'successfactors.com',
    'gusto.com',
    'bonusly.com',
    'cultureamp.com',
    'nectar.com',
    'lattice.com'
]

# Connect to the database
conn = sqlite3.connect('website_blocker.db')
cursor = conn.cursor()

# Convert websites to IP addresses and insert into 'Top25WorkSites' table
for site in work_sites:
    try:
        ip_address = socket.gethostbyname(site)
        cursor.execute("INSERT INTO Top25WorkSites (site_name) VALUES (?)", (ip_address,))
    except socket.error as e:
        print(f"Error converting {site} to IP address: {e}")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted into Top25WorkSites table.")

