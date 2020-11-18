#Imports & Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import time

#Site Navigation
executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)


# Defining scrape & dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data

time.sleep(2)


NASA Mars News
def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html_news = browser.html
    soup = BeautifulSoup(html_news, "html.parser")
    news = soup.find("li", class_="slide")
    news_title = news.find("div", class_="content_title").text
    news_p = news.find("div", class_="article_teaser_body").text
    output = [news_title, news_p]

    return output  

time.sleep(2)


# JPL Mars Space Images - Featured Image
def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    browser.click_link_by_id("full_image")
    browser.click_link_by_partial_text("more info")
    html_image = browser.html
    soup = BeautifulSoup(html_image, 'html.parser')
    image = soup.select_one('figure', class_="lede")
    image_url = image.select_one("a").get("href")
    featured_image_url = "https://www.jpl.nasa.gov"+ image_url 

    return featured_image_url

time.sleep(2) 


# Mars Facts
def marsFacts():
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_data.columns = ["Description", "Value"]
    mars_data = mars_data.set_index("Description")
    mars_facts = mars_data.to_html(index = True, header =True)

    return mars_facts

time.sleep(2)


# Mars Hemispheres
def marsHem():
    import time 
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html_hem = browser.html
    soup = BeautifulSoup(html_hem, "html.parser")

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
        dictionary = {"title": title, "img_url": image_url}
        mars_hemisphere.append(dictionary)

        return mars_hemisphere
        
time.sleep(2)