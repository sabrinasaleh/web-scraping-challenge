#Imports & Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import time

#Site Navigation
executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)


# Defining scrape
def scrape():
    # NASA Mars News
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html_news = browser.html
    soup = BeautifulSoup(html_news, "html.parser")
    news = soup.find("li", class_="slide")
    news_title = news.find("div", class_="content_title").get_text
    news_p = news.find("div", class_="article_teaser_body").get_text
    
    time.sleep(1)


     # JPL Mars Space Images - Featured Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    browser.click_link_by_id("full_image")
    browser.click_link_by_partial_text("more info")
    html_image = browser.html
    soup = BeautifulSoup(html_image, 'html.parser')
    image = soup.select_one('figure', class_="lede")
    image_url = image.select_one("a").get("href")
    featured_image_url = "https://www.jpl.nasa.gov"+ image_url 

    time.sleep(1)
    

    # Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_data.columns = ["Description", "Value"]
    mars_data = mars_data.set_index("Description")
    mars_facts = mars_data.to_html(index = True, header =True)

    time.sleep(1)


    # Mars Hemispheres 
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

        time.sleep(1)


# Defining dictionary
    mars_dict = {
        "mars_news": news_title,
        "mars_paragraph": news_p,
        "mars_image": featured_image_url, 
        "mars_facts": mars_facts,
        "mars_hemisphere": mars_hemisphere,
    } 
    

    return mars_dict

