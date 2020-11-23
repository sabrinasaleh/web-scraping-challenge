#Imports & Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

#Site Navigation
executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)


# NASA Mars News
news_url = "https://mars.nasa.gov/news/"
browser.visit(news_url)
html_news = browser.html
soup = BeautifulSoup(html_news, "html.parser")
# Retrieve the latest element that contains news title and news_paragraph
news = soup.find("li", class_="slide")
news_title = news.find("div", class_="content_title").get_text
news_p = news.find("div", class_="article_teaser_body").get_text
# Display scrapped data for news_title and news_p 
print(news_title)
print(news_p)


# JPL Mars Space Images - Featured Image
image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(image_url)
browser.click_link_by_id("full_image")
browser.click_link_by_partial_text("more info")
html_image = browser.html
soup = BeautifulSoup(html_image, 'html.parser')
# Retrieve the url for featured_image 
image = soup.select_one('figure', class_="lede")
image_url = image.select_one("a").get("href")
# Display complete url string for the featured_image
print("https://www.jpl.nasa.gov"+ image_url)


# Mars Facts
facts_url = "https://space-facts.com/mars/"
browser.visit(facts_url)
# Use pandas to convert the data to a HTML table string
mars_data = pd.read_html(facts_url)
mars_data = pd.DataFrame(mars_data[0])
mars_facts = mars_data.to_html(header = False, index = False)
# Display the HTML table string
print(mars_facts)


# Mars Hemispheres
hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemispheres_url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")
# Retrive the dictionary of hemispheres with title and image_url
mars_hemisphere = []
products = soup.find("div", class_ = "result-list" )
hemispheres = products.find_all("div", class_="item")

for hemisphere in hemispheres:
    title = hemisphere.find("h3").text
    title = title.replace("Enhanced", "")
    end_link = hemisphere.find("a")["href"]
    image_link = "https://astrogeology.usgs.gov/" + end_link    
    browser.visit(image_link)
    html = browser.html
    soup=BeautifulSoup(html, "html.parser")
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    mars_hemisphere.append({"title": title, "img_url": image_url})
    
# Diaplay the dictionary
print(mars_hemisphere)