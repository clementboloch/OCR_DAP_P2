# OCR_DAP_P2
Développeur d'Application Python - Projet 2



## Presentation

This project gives a set of functions to scrap the "Books to Scrape" website (http://books.toscrape.com/index.html).
The `scrap` function allows you to scrap the entire website.



## Setup

### Directory setup
It is recommended to create a dedicated directory to download the project.
In a terminal:
`mkdir dir_name`

### Git setup
Initialize your local Git repository. In a terminal (in your dedicated directory):
`git init`

Then clone the remote repository in your local repository with the https link. You will find the https link is in the "code" drop-down menu:
`git clone https_project_link`

### Virtual environment setup
It is recommended to set a virtual environment before installing the dependencies:
`python3.9 -m venv env`

To activate your virtual environment:
`source env/bin/activate`

Then, you can install the python dependencies for the project: 
`pip install -r requirements.txt`


## Scrap the website 

To scrap the "Books to Scrape" website (http://books.toscrape.com/index.html):
`python3.9 exec.py`

If the script execution has started, "start scrapping ..." will be printed in your terminal. The scrapping takes approximately 15 minutes for 1000 books. At the end of the execution, a tuple of the following form will be printed in your terminal:
`(True, '900')`
The first element is a boolean: "True" if the scrapping is complete, "False" if an error occurred. The second element is the execution time in second.

The script automatically create directories and files to save the scrapped data. In the current directory, a directory named "results" is created, with two other directories inside : "csvs" and "images". 
A csv is created for each category scrapped one the website, and is stored in the "csvs" directory. Each csv has the same columns :
- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

The image of each book is saved in the "images" directory as jpg files.