import requests
from bs4 import BeautifulSoup
import csv

# We need url to send a request to the server and get the content of the page. 
# We will use the requests library to do this.
url = 'https://books.toscrape.com/'

# Saving the response of the request in a variable called response. 
# The response variable will contain the content of the page that we requested.
response = requests.get(url)

# Checking the status code of the response to see if the request was successful.
print(response.status_code)  # A status code of 200 means the request was successful.

# The content of the page is in HTML format, so we need to parse it to extract the information we need. 
# We will use the BeautifulSoup library to do this.
soup = BeautifulSoup(response.content, 'html.parser')


# Now we will make program to extract title of book, price of book and link to the book.
# We will use the find_all method of BeautifulSoup to find all the elements that contain the information we need. 
# The find_all method takes the name of the tag and the class name as arguments and returns a list of all the elements that match the criteria.

book_title = soup.find_all('h3')

book_price = soup.find_all('p', class_='price_color')

book_links = soup.find_all('a', href=True)

complete_data = []
for titles, price, links in zip(book_title, book_price, book_links):
    book_title = titles.text
    book_price = price.text
    book_link = links['href']
    complete_data.append([book_title, book_price, book_link])
    

# Now we will save the extracted information in a CSV file in simple format.

with open('books.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Link'])
    writer.writerows(complete_data)