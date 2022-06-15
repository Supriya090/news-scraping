import json
import requests
import sqlite3

# making the API request
def searchJSON(searchTerm, url, pageNum):
    params = dict(
        title=searchTerm,
        page=pageNum
    )
    resp = requests.get(url=url, params=params)
    data = resp.json()
    return data


# getting the latest page_number based on the search term
def getCurrentPage(searchRows, searchTerm):
    currentPage = 0
    if(len(searchRows) != 0):
        currentTerm = searchRows[-1][0]
        if(str(currentTerm) != searchTerm):
            currentPage = 0
        else:
            currentPage = searchRows[-1][1]
    print("Current Page: ", currentPage)
    return currentPage


def main():
    # creating and connecting to annapurna db
    connection = sqlite3.connect("annapurna.db")
    if (connection.total_changes == 0):
        print("DB Connected")

    # creating a cursor
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS news (searchTerm STRING, JSON TEXT, page_number INTEGER)")

    # getting news with user-specified search term
    searchTerm = input("Enter the term you want to search: ")
    searchRows = cursor.execute(
        "SELECT searchTerm, page_number FROM news").fetchall()
    currentPage = getCurrentPage(searchRows, searchTerm)
    pages = currentPage + 1     # just for making the first loop

    # pagination
    url = "https://bg.annapurnapost.com/api/search"
    i = currentPage
    while i <= pages:
        eachData = searchJSON(searchTerm, url, i+1)
        if(i == currentPage):
            pages = eachData['data']['totalPage']
        # storing page_number after each response
        cursor.execute("INSERT INTO news (searchTerm, JSON, page_number) VALUES (?, ?, ?)",
                       (searchTerm, json.dumps(eachData), i+1,))
        connection.commit()
        print(eachData)
        print("\n\n\n")
        i += 1


if __name__ == "__main__":
    main()
