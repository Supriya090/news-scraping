import sys
import requests
import sqlite3
import math

# creating and connecting to annapurna db
connection = sqlite3.connect("annapurna.db")
print(connection.total_changes)

# creating a cursor
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS news (searchTerm STRING, page_number INTEGER)")


# getting news with user-specified search term
searchTerm = input("Enter the term you want to search: ")
url = "https://bg.annapurnapost.com/api/search"
params = dict(
    title=searchTerm,
)
resp = requests.get(url=url, params=params)
data = resp.json()


# getting total number of pages
total = data['data']['total']
count = data['data']['count']
print("Total number of articles of the search term \"",
      searchTerm, "\" is : ", total)
if(total == 0):
    print("No article with the given search term exists")
    sys.exit()
pages = math.ceil(total/count)

currentPage = 0


# getting the latest page_number based on the search term
searchRows = cursor.execute(
    "SELECT searchTerm, page_number FROM news").fetchall()
if(len(searchRows) != 0):
    currentTerm = searchRows[-1][0]
    if(str(currentTerm) != searchTerm):
        currentPage = 0
    else:
        currentPage = searchRows[-1][1]

print(currentPage)

if (currentPage == pages):
    print("All articles displayed")


# pagination
for i in range(currentPage, pages):
    pageParams = dict(
        title=searchTerm,
        page=i+1
    )
    eachResp = requests.get(url=url, params=pageParams)
    eachData = eachResp.json()
    # storing page_number after each response
    cursor.execute("INSERT INTO news (searchTerm, page_number) VALUES (?, ?)",
                   (searchTerm, i+1,))
    connection.commit()
    print(eachData)
    print("\n\n\n")
