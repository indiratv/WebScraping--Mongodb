### Step 2 - MongoDB and Flask Application

## Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

# Dependencies
from bs4 import BeautifulSoup
import requests
import json
from splinter import Browser
# Initialize Tweepy for Twitter Analysis
import tweepy
import json
# Importing Pandas for Pandas Scraping
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    marsdata_dict = {}
# 1.Get Latest News Title and Para
    url = 'https://mars.nasa.gov/news/'
    time.sleep(5)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_title = soup.find('div', class_="content_title").text.strip()
    news_p = soup.find('div', class_="rollover_description_inner").text.strip()
    marsdata_dict["news_title"] = news_title
    marsdata_dict["news_p"] = news_p
# 2.Get the featured Image url   
    browser = Browser('chrome', headless=False)
    urli = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(urli)
    time.sleep(5)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Click the 'FULL IMAGE' button on the featured image on the home page
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    imagesrc = soup.find('figure', class_='lede').find('img')['src']
    featured_image_url = "https://www.jpl.nasa.gov" + imagesrc
    marsdata_dict["featured_image_url"] = featured_image_url
# 3.Get the mars weather data from latest tweet   

    consumer_key = "wNC3lUy34Zm8YYOkzhgRWXo0A"
    consumer_secret = "Tgs4zKsSW05KmVhuZdvtXy3V7KXbGZdJJsG6BeWv3BwOl1CjGL"
    access_token = "943239523047235584-OhbdaN1nJYFHzrpVBbFzOMTxbQaRDaj"
    access_token_secret = "Rinpous00RQFCnvVMNWKxOgQZE5H0wxJ2GtjWSHGgq0uW"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    target_user = "@MarsWxReport"
    public_tweets = api.user_timeline(target_user,count=1)
    mars_weather = public_tweets[0]["text"]
    marsdata_dict["mars_weather"] = mars_weather

# 4.Get the mars facts

    marsurl = "https://space-facts.com/mars/"
    tables = pd.read_html(marsurl)
    df = tables[0]
    df.columns = ['Parameter', 'Value']
    df.set_index('Parameter', inplace=True)
    html_table = df.to_html()
    marsdata_dict["mars_facts"] = html_table

# 5.Get the mars hemispheres titles and images

    urlmh = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser = Browser('chrome', headless=False)
    browser.visit(urlmh)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemlinks = soup.find_all('div', class_='description')
    # console.log(hemlinks)
    hemisphere_image_urls = []

    for link in hemlinks:
        title = link.find('h3').text.strip(' Enhanced')
        # console.log(title);
        urlh = "https://astrogeology.usgs.gov" + link.find('a')['href']
        browser.visit(urlh)
        time.sleep(5)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        imageurl = soup.find('div', class_='downloads').find('li').find('a')['href']
        # console.log(imageurl)
        hemisphere_image_urls.append({"title": title,"img_url": imageurl})
        marsdata_dict["hemisphere_image_urls"] = hemisphere_image_urls  
        urlh = ""   

    return marsdata_dict