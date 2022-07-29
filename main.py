''''
====================================
To be scrapped in every product page
====================================
product_page_url
universal_ product_code (upc)
title
price_including_tax
price_excluding_tax
number_available
product_description
category
review_rating
image_url

--> product_page_url --> PARENT SCRAPPING
category --> PARENT SCRAPPING
title --> OK
review_rating --> OK
image_url --> OK
product_description --> OK
    universal_ product_code (upc) --> OK
    price_excluding_tax --> OK
    price_including_tax --> OK
    number_available --> OK 



======
Output
====== 
-> csv file

'''

import csv
import requests
from bs4 import BeautifulSoup as BS

product_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

def def_soup(product_url):
    response = requests.get(product_url)
    if response.ok:
        soup = BS(response.text, "html.parser")
        return soup
    else:
        return None

# Try again every x sec if not true --> else : delay, call back the finction + counter to stop if bug 
# Except with some response ? ex 404
# Use proxy instaid of delay ?
    

# TITLE
def title(soup):
    title = soup.find('div', {'class': 'product_main'}).find('h1').text
    return title

# REVIEW RATING
def rating(soup):
    rate_dict = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    rating_list = soup.find('p', {'class': 'star-rating'})['class']

    rating = 0
    for val in rating_list:
        if val in rate_dict.keys():
            rating = rate_dict.get(val)
            rating = str(rating)
            break
    if not rating:
        rating = "No rating found"

    return rating


# IMAGE_URL
def image(soup):
    image = soup.find('img')['src']
    image = image.replace('../../', 'http://books.toscrape.com/')
    return image

# PRODUCT DESCRIPTION
def description(soup):
    description = soup.find('div', {'id': 'product_description'}).find_next_sibling('p').text
    return description

# TABLE
def def_table(soup):
    table = soup.find('table', {'class':'table-striped'})
    ths = [th.text.lower().strip() for th in table.findAll('th')]
    tds = [td.text.lower().strip() for td in table.findAll('td')]

    table = dict(zip(ths, tds))
    return table

def upc(table):
    return table.get("upc")

def price_e(table):
    pe_brut = table.get("price (excl. tax)")
    pe_list = [ele for ele in pe_brut if ele.isdigit() or ele == "." or ele == ","]
    pe_cleaned = ''.join(pe_list).replace(",", ".")
    return pe_cleaned

def price_i(table):
    pi_brut = table.get("price (incl. tax)")
    pi_list = [ele for ele in pi_brut if ele.isdigit() or ele == "." or ele == ","]
    pi_cleaned = ''.join(pi_list).replace(",", ".")
    return pi_cleaned

def availability(table):
    av_brut = table.get("availability")
    av_list = filter(str.isdigit, av_brut)
    av_cleaned = ''.join(av_list)
    return av_cleaned

def csv_comp(text):
    return '"' + text + '"'

def scrap(url, category):
    soup = def_soup(url)
    table = def_table(soup)

    row = []
    row.append(url)
    row.append(upc(table))
    row.append(csv_comp(title(soup)))
    row.append(price_i(table))
    row.append(price_e(table))
    row.append(availability(table))
    row.append(csv_comp(description(soup)))
    row.append(csv_comp(category))
    row.append(rating(soup))
    row.append(image(soup))
    
    return row

def csv_init(file):
    row = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
    with open(file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(row)

def save(row, file):
    try:
        with open(file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(row)
    except:
        return False

scrapped_text = scrap(product_url, "test")
csv_init("./test.csv")
save(scrapped_text, "./test.csv")