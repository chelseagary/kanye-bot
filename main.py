from bot import Bot
from db import DB

# create database file
db_filename = 'database.db'
f = open(db_filename, 'w')
f.write('')
f.close()

# fill database with response (can take awhile depending on how big database is)
database = DB(db_filename)
create = 'CREATE TABLE Responses (keyword TEXT PRIMARY KEY, response TEXT NOT NULL, priority INTEGER NOT NULL);'
database.create_table(create)
with open("responses.txt", "r") as txt:
    for line in txt:
        if line == '':
            continue
        if line.count('//') != 2:
            continue
        message = line.split('//')
        keyword = str(message[0]).strip()
        response = str(message[1]).strip()
        priority = int(message[2])
        x = (keyword, response, priority)
        database.insert_response(x)

# Get API token
f = open('token', 'r')
api_token = f.readline()
f.close()

# Initialize bot and begin running
Kanye = Bot(api_token, db_filename)
print("Bot is up and running...")
while True:
    Kanye.run()