#Imports & Dependencies
from splinter import Browser
from bs4 import BeautifulSoup

#Site Navigation
executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)

#NASA Mars News
url = "https://mars.nasa.gov/news/"
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")

# Search for news titles
title_results = soup.find_all('div', class_='content_title')

# Search for paragraph text under news titles
p_results = soup.find_all('div', class_='article_teaser_body')

# Extract first title and paragraph, and assign to variables
news_title = title_results[0].text
# news_p = p_results[0].text

print(news_title)
# print(news_p)