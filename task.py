import requests
import sqlite3
import math

# creating and connecting to annapurna db
connection = sqlite3.connect("annapurna.db")
print(connection.total_changes)

# creating a cursor
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS news (page_number INTEGER)")

# getting news with search term "1"
url = "https://bg.annapurnapost.com/api/search"
params = dict(
    title='1',
)
resp = requests.get(url=url, params=params)
data = resp.json()

# getting total number of pages
total = data['data']['total']
count = data['data']['count']
pages = math.ceil(total/count)
currentPage = 0

# getting the latest page_number
value = cursor.execute("SELECT page_number FROM news").fetchall()
if(len(value) != 0):
    currentPage = value[-1][0]

print(currentPage)


# pagination
for i in range(currentPage, pages):
    pageParams = dict(
        title='1',
        page=i+1
    )
    eachResp = requests.get(url=url, params=pageParams)
    eachData = eachResp.json()
    # storing page_number after each response
    cursor.execute("INSERT INTO news (page_number) VALUES (?)",
                   (i+1,))
    connection.commit()
    print(eachData)
    print("\n\n\n")
