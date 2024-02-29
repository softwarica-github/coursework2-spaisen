import sqlite3
import socket

# List of social media websites
social_sites = [
    'facebook.com',
    'youtube.com',
    'whatsapp.com',
    'instagram.com',
    'wechat.com',
    'tiktok.com',
    'messenger.com',
    'telegram.org',
    'snapchat.com',
    'douyin.com',
    'kuaishou.com',
    'weibo.com',
    'qq.com',
    'twitter.com',
    'reddit.com',
    'pinterest.com',
    'josh.com',
    'twitch.com',
    'discord.com',
    'likee.com',
    'picsart.com',
    'vevo.com',
    'tumblr.com',
    'vk.com'
]

# Connect to the database
conn = sqlite3.connect('website_blocker.db')
cursor = conn.cursor()

# Convert websites to IP addresses and insert into 'Top25SocialSites' table
for site in social_sites:
    try:
        ip_address = socket.gethostbyname(site)
        cursor.execute("INSERT INTO Top25SocialSites (site_name) VALUES (?)", (ip_address,))
    except socket.error as e:
        print(f"Error converting {site} to IP address: {e}")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted into Top25SocialSites table.")
