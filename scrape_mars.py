from splinter import Browser
from bs4 import BeautifulSoup
import time

import pandas as pd

from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

import re

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # executable_path = {"executable_path": "C:\Users\Mary-Dave\Anaconda3\pkgs\selenium-chromedriver-2.27-0\Library\bin\chromedriver"}
    executable_path = {"executable_path": "./chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # NASA Mars News Site URL
    nasa_mars_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    #time.sleep(1)

    # Scrape page into Soup
    browser.visit(nasa_mars_url)
    nasa_mars_html = browser.html
    nasa_mars_soup = BeautifulSoup(nasa_mars_html, 'html.parser')

    # results are returned as an iterable list
    nasa_mars_results = nasa_mars_soup.find_all('div', class_='list_text')

    # Get most recent news title and paragraph
    news_title = nasa_mars_results[0].a.text
    news_p = nasa_mars_results[0].find('div', class_='article_teaser_body').text



    # NASA JPL Site URL
    nasa_jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(nasa_jpl_url)

    nasa_jpl_html = browser.html
    nasa_jpl_soup = BeautifulSoup(nasa_jpl_html, 'html.parser')

    nasa_jpl_results = nasa_jpl_soup.find_all('article', class_='carousel_item')

    # Get the JPL featured image
    featured_image_url = 'https://www.jpl.nasa.gov' + nasa_jpl_results[0].find('a', class_='button fancybox')['data-fancybox-href']



    # Twitter URL
    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(twitter_url)

    twitter_html = browser.html
    twitter_soup = BeautifulSoup(twitter_html, 'html.parser')

    twitter_results = twitter_soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    # Get latest tweet for Mars weather
    mars_weather = ''
    for tweet in twitter_results:
        # exclude text from "a" tag
        if tweet.find('a'):
            tweet.find('a').extract()
    
        # find first tweet that starts with 'InSight sol '
        rex = re.compile('InSight sol *')
        if rex.findall(tweet.text):
            mars_weather = tweet.text
            break



    # Mars Facts URL
    mars_facts_url = 'https://space-facts.com/mars/'

    mars_facts_df_list = pd.read_html(mars_facts_url)

    mars_facts_df = mars_facts_df_list[0]

    mars_facts_df.rename(columns={mars_facts_df.columns[0]:'Description', mars_facts_df.columns[1]:'Value'}, inplace=True)

    # Convert Mars facts data frame to HTML table
    mars_facts_html_table = mars_facts_df.to_html(index=False)



    # USGS Astrogeology URL
    #usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #browser.visit(usgs_url)

    #usgs_html = browser.html
    #usgs_soup = BeautifulSoup(usgs_html, 'html.parser')

    usgs_cerberus_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    usgs_schiaparelli_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    usgs_syrtis_major_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    usgs_valles_marineres_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    browser.visit(usgs_cerberus_url)

    usgs_cerberus_html = browser.html
    usgs_cerberus_soup = BeautifulSoup(usgs_cerberus_html, 'html.parser')

    usgs_cerberus_results = usgs_cerberus_soup.find_all('a')

    for result in usgs_cerberus_results:
        if result.text == 'Sample':
            usgs_cerberus_image = result['href']

    usgs_cerberus_title_results = usgs_cerberus_soup.find_all('h2', class_='title')

    usgs_cerberus_title = usgs_cerberus_title_results[0].text

    browser.visit(usgs_schiaparelli_url)
    usgs_schiaparelli_html = browser.html
    usgs_schiaparelli_soup = BeautifulSoup(usgs_schiaparelli_html, 'html.parser')
    usgs_schiaparelli_results = usgs_schiaparelli_soup.find_all('a')
    for result in usgs_schiaparelli_results:
        if result.text == 'Sample':
            usgs_schiaparelli_image = result['href']

    usgs_schiaparelli_title_results = usgs_schiaparelli_soup.find_all('h2', class_='title')
    usgs_schiaparelli_title = usgs_schiaparelli_title_results[0].text

    browser.visit(usgs_syrtis_major_url)
    usgs_syrtis_major_html = browser.html
    usgs_syrtis_major_soup = BeautifulSoup(usgs_syrtis_major_html, 'html.parser')
    usgs_syrtis_major_results = usgs_syrtis_major_soup.find_all('a')
    for result in usgs_syrtis_major_results:
        if result.text == 'Sample':
            usgs_syrtis_major_image = result['href']

    usgs_syrtis_major_title_results = usgs_syrtis_major_soup.find_all('h2', class_='title')
    usgs_syrtis_major_title = usgs_syrtis_major_title_results[0].text

    browser.visit(usgs_valles_marineres_url)
    usgs_valles_marineres_html = browser.html
    usgs_valles_marineres_soup = BeautifulSoup(usgs_valles_marineres_html, 'html.parser')
    usgs_valles_marineres_results = usgs_valles_marineres_soup.find_all('a')
    for result in usgs_valles_marineres_results:
        if result.text == 'Sample':
            usgs_valles_marineres_image = result['href']

    usgs_valles_marineres_title_results = usgs_valles_marineres_soup.find_all('h2', class_='title')
    usgs_valles_marineres_title = usgs_valles_marineres_title_results[0].text

    hemisphere_image_urls = [
        {"title": usgs_valles_marineres_title, "img_url": usgs_valles_marineres_image},
        {"title": usgs_cerberus_title, "img_url": usgs_cerberus_image},
        {"title": usgs_schiaparelli_title, "img_url": usgs_schiaparelli_image},
        {"title": usgs_syrtis_major_title, "img_url": usgs_syrtis_major_image},
    ]

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts_html_table": mars_facts_html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
