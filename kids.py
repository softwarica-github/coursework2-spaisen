import sqlite3
import socket

# List of kids websites
kids_sites = [
    'khanacademy.org',
    'nasa.gov',
    'theconsciouskid.org',
    'cryptoclub.org',
    'jumpstarttestprep.com',
    'nationalzoo.si.edu',
    'playclassic.games',
    'duolingo.com',
    'myhero.com',
    'stopdisastersgame.org',
    'gridclub.com',
    'fascinatingeducation.com',
    'abookintime.net',
    'learninglab.si.edu',
    'kids.nationalgeographic.com',
    'makemegenius.com',
    'earth.google.com',
    'bedtimemath.org',
    'scratch.mit.edu',
    'wizardingworld.com',
    'pbskids.org',
    'amightygirl.com',
    'superkidsnutrition.com',
    'friendzy.co',
    'starfall.com',
    'youtubekids.com'
]

# Connect to the database
conn = sqlite3.connect('website_blocker.db')
cursor = conn.cursor()

# Convert websites to IP addresses and insert into 'Top25KidsSites' table
for site in kids_sites:
    try:
        ip_address = socket.gethostbyname(site)
        cursor.execute("INSERT INTO Top25KidsSites (site_name) VALUES (?)", (ip_address,))
    except socket.error as e:
        print(f"Error converting {site} to IP address: {e}")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted into Top25KidsSites table.")

