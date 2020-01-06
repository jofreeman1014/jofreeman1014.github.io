from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import time
import pandas as pd
import lxml

def scraper(): 


    # Initialize PyMongo to work with MongoDBs
    #conn = 'mongodb://localhost:27017'
    #client = pymongo.MongoClient(conn)
    # # Define database and collection
    # db = client.craigslist_db
    # collection = db.items
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Mars News
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mars_title = soup.body.find('div',attrs={"class" : "content_title"}).text.replace('\n', '') # !!
    mars_body = soup.body.find('div',attrs={"class" : "rollover_description_inner"}).text.replace('\n', '') # !!

    # Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mars_tweets=soup.find_all("p", attrs = {"class":"TweetTextSize"})
    for item in mars_tweets:
        if "InSight sol" in item.text:
            mars_weather = item.text # !!
            break

    # Mars Featured Image
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1.3)
    browser.click_link_by_partial_text('more info')
    time.sleep(1.3)
    browser.click_link_by_partial_text('.jpg')
    featured_image_url = browser.url # !!
    browser.quit()

    # Mars Facts

    url = 'https://space-facts.com/mars/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = pd.read_html(url)
    tables[1]
    mars_table = tables[1].to_html(index = False,header = False) # !!


    # Mars Hemisphere
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    browser.visit(url)
    mars_hemi_img=[]
    mars_hemi=soup.find_all("a", attrs = {"class":"itemLink product-item"})

    for item in mars_hemi:
        if item.has_attr('href'):
            tmp = item.text
            browser.click_link_by_partial_text(tmp)
            tmp_res = requests.get(browser.url)
            soup = BeautifulSoup(tmp_res.text, 'html.parser')
            tmp_url = soup.find_all("a",href = True)
            for item in tmp_url:
                if "Sample" in item.text:
                    mars_hemi_img.append({"title":tmp,"img_url":item['href']})#browser.url})
                    break

            browser.back()
            #time.sleep(0.5)
    browser.quit()

    mars_data = {
        "news_title": mars_title, #string X
        "news_body": mars_body, #string X
        "weather": mars_weather, #string X
        "image": featured_image_url, #url X
        "facts": mars_table, #html table X
        "hemi": mars_hemi_img #list of dictionaries X
    }
    return mars_data


