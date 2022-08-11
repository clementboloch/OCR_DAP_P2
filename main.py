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

======
Output
====== 
-> csv file

'''

from pathlib import Path
import csv

import requests
from bs4 import BeautifulSoup as BS

curr_dir_path = Path.cwd()

'''
====================
SCRAP A PRODUCT PAGE
====================
'''

def def_soup(url):
    response = requests.get(url)
    if response.ok:
        soup = BS(response.text, "html.parser")
        return soup
    else:
        return None

# TITLE
def title(soup):
    try :
        title = soup.find('div', {'class': 'product_main'}).find('h1').text
        return title
    except : 
        return "!!! No title found !!!"

# CATEGORY
def category(soup):
    try :
        category = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].string
        return category
    except : 
        return "!!! No category found !!!"

# REVIEW RATING
def rating(soup):
    rate_dict = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    try :
        rating_list = soup.find('p', {'class': 'star-rating'})['class']
        rating = 0
        for val in rating_list:
            if val in rate_dict.keys():
                rating = rate_dict.get(val)
                rating = str(rating)
                break
        if not rating:
            rating = "!!! No rating found !!!"
        return rating
    except : 
        return "!!! No rating found !!!"


# IMAGE_URL
def image(soup):
    try :
        image_url = soup.find('img')['src']
        image_url = image_url.replace('../../', 'http://books.toscrape.com/')
        return image_url
    except : 
        return "!!! No image found !!!"

# PRODUCT DESCRIPTION
def description(soup):
    try :
        description = soup.find('div', {'id': 'product_description'}).find_next_sibling('p').text
        return description
    except : 
        return "!!! No description found !!!"

# TABLE
def def_table(soup):
    try :
        table = soup.find('table', {'class':'table-striped'})
        ths = [th.text.lower().strip() for th in table.findAll('th')]
        tds = [td.text.lower().strip() for td in table.findAll('td')]

        table = dict(zip(ths, tds))
        return table
    except : 
        return None

def upc(table):
    try :
        return table.get("upc")
    except : 
        return "!!! No UPC found !!!"

def price_e(table):
    try :
        pe_brut = table.get("price (excl. tax)")
        pe_list = [ele for ele in pe_brut if ele.isdigit() or ele == "." or ele == ","]
        pe_cleaned = ''.join(pe_list).replace(",", ".")
        return pe_cleaned
    except : 
        return "!!! No price (excl. tax) found !!!"

def price_i(table):
    try :
        pi_brut = table.get("price (incl. tax)")
        pi_list = [ele for ele in pi_brut if ele.isdigit() or ele == "." or ele == ","]
        pi_cleaned = ''.join(pi_list).replace(",", ".")
        return pi_cleaned
    except : 
        return "!!! No price (incl. tax) found !!!"

def availability(table):
    try :
        av_brut = table.get("availability")
        av_list = filter(str.isdigit, av_brut)
        av_cleaned = ''.join(av_list)
        return av_cleaned
    except : 
        return "!!! Availability not found !!!"

def csv_comp(text):
    text = text.replace(";",",")
    text = text.replace("/","-")
    return '"' + text + '"'

def scrap_product(url, dl_img = False):
    soup = def_soup(url)
    table = def_table(soup)

    img = image(soup)
    cat = category(soup)
    name = csv_comp(title(soup))

    row = []
    row.append(url)
    row.append(upc(table))
    row.append(name)
    row.append(price_i(table))
    row.append(price_e(table))
    row.append(availability(table))
    row.append(csv_comp(description(soup)))
    row.append(cat)
    row.append(rating(soup))
    row.append(img)
    
    if dl_img:
        result = (row, (img, f"{cat} - {name}"))
    else:
        result = (row)

    return result


'''
==================
SAVE IN A CSV FILE 
==================
'''

def define_path(root_dir_path:str = ""):
    if root_dir_path:
        try:
            root_path = Path(root_dir_path)
        except:
            root_path = curr_dir_path
    else:
        root_path = curr_dir_path
    return root_path

def create_dirs(dirs:list = [], root_dir_path:str = ""):
    root_path = define_path(root_dir_path)
    dir_path = root_path.joinpath(*dirs)
    dir_path.mkdir(exist_ok=True, parents=True)
    return dir_path

def csv_init(dirs:list = [], category:str = "unknown", root_dir_path:str = ""):
    row = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
    dir_path = create_dirs(dirs, root_dir_path)
    file_path = dir_path/f"{category}.csv"
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(row)
    return file_path

def save(row, file_path):
    try:
        with open(file_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        return True
    except:
        return False

# rapport : essayer de faire des fonctions homogènes : si return False si bug, return True si fonctionne

'''
=====================
SCRAP A CATEGORY PAGE 
=====================
In-put : category url
Out-put : list of product url

Find the product url with the class "product_prod"
Loop in a loop : product in the page inside the number page of the category
'''

def products_url(soup):
    articles = soup.findAll('article', {'class': 'product_pod'})#.find('a')['href']
    
    urls = []
    for article in articles:
        url = article.find('a')['href']
        url = url.replace('../../../', 'https://books.toscrape.com/catalogue/')
        urls.append(url)
    
    return urls

def next_page(soup, category_url):
    category_url = category_url.replace('index.html','')
    next_class = soup.find('li', {'class': 'next'})
    if next_class:
        next_url = next_class.find('a')['href']
        next_url = category_url + next_url
        return next_url
    else:
        return None

# PRINCIPAL FUNCTION
def scrap_category(category_url):
    books_url = []
    soup = def_soup(category_url)
    n_p = next_page(soup, category_url)
    while n_p:
        p_u = products_url(soup)
        books_url.extend(p_u)
        soup = def_soup(n_p)
        n_p = next_page(soup, category_url)
    p_u = products_url(soup)
    books_url.extend(p_u)
    return books_url
    

'''
Remarque :
J'ai hésité à créer une liste qui contiendrait l'ensemble des url de chaque page des produits, pour boucler ensuite dessus
Mais ça impliquerait de faire 2 fois plus de requête de page : une fois pour les stocker, une autre pour les parser
'''

'''
====================
SCRAP ALL CATEGORIES 
====================
'''

def find_categories(site_url):
    soup = def_soup(site_url)
    nav = soup.find('ul', {'class': 'nav-list'}).find('ul').findAll('li')
    categories = ['https://books.toscrape.com/' + url.find('a')['href'] for url in nav]
    return categories


'''
===============
DOWNLOAD IMAGES
===============
'''

def dl_image(img_url:str, img_name:str = "unknown", dirs:list = [], root_dir_path:str = ""):
    dir_path = create_dirs(dirs, root_dir_path)
    img_path = dir_path/f"{img_name}.jpg"
    response = requests.get(img_url)
    if response.ok:
        with open(img_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False



'''
=========
SCRAP ALL 
=========
'''

def scrap(site_url, path, dl_img = False):
    categories_url = find_categories(site_url)
    for category_url in categories_url:
        books_url = scrap_category(category_url)
        first_run = True
        file_path = ""
        for book_url in books_url:
            s_p = scrap_product(book_url, dl_img)
            row = s_p[0]
            category = row[7]
            if first_run:
                file_path = csv_init(['results', 'csvs'], category)
                first_run = False
            save(row, file_path)
            if dl_img:
                try :
                    img_url = s_p[1][0]
                    img_name = s_p[1][1]
                    dl_image(img_url, img_name, ['results', 'images'])
                except:
                    return False
    return True