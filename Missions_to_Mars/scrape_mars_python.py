
# Stage 1 - Scraping Lift Off!

# %%
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo
import pandas as pd


def scrape():
# %%
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


# NASA Mars News
#--------------------------------------------------------------------------------------------------------------------------------------------------

# %%
# Source Scrape URL 
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)


# %%
# Retrieve page
    news_retrieve = requests.get(news_url)

# Create BeautifulSoup object
    news_soup = BeautifulSoup(news_retrieve.text, 'html.parser')

    news_html = browser.html
    news_results = BeautifulSoup(news_html, 'html.parser')


# %%
# Retrieve headline and flavor text
    news_title = news_results.find('div', class_='content_title').get_text()
    news_teaser = news_results.find('div', class_='article_teaser_body').get_text()

    print(news_title)
    print(news_teaser)


# JPL Mars Space Images - Featured Image
#-----------------------------------------------------------------------------------------------------------------------------------------------

# %%
# Source Scrape URL 
    images_url = 'https://spaceimages-mars.com/'
    browser.visit(images_url)

# %%
# Retrieve page
    images_retrieve = requests.get(images_url)

# Create BeautifulSoup object
    images_soup = BeautifulSoup(images_retrieve.text, 'html.parser')

    images_html = browser.html
    soup = BeautifulSoup(images_html, 'html.parser')

    for div in soup.find_all('div', class_='floating_text_area'):
        a = div.find('a')
        image = a['href']
    
    # Get the featured image url
    featured_image_url = 'https://spaceimages-mars.com/' + image
    
# %%
# Retrieve Current Header Image from URL 
    # featured_image = images_results.find('img', class_='headerimage')
    # featured_image = featured_image['src']

    # print(featured_image)

# Mars Facts
#--------------------------------------------------------------------------------------------------------------------------------------------------

# %%
# Source Scrape URL 
    facts_url = 'https://galaxyfacts-mars.com/'
    
# %%
    tables = pd.read_html(facts_url)
    tables


# %%
#Set table data into Dataframe
    facts_df = tables[0]
    facts_df.head(20)


# %%
#Renamed Columns
    facts_df.rename(columns={0:'Index', 1: 'Mars Value', 2: 'Earth Values'})


# %%
#Converted DataFrame into HTML string
    facts_html = facts_df.to_html()
    print(facts_html)


# Mars Hemishperes
#-----------------------------------------------------------------------------------------------------------------------------------------------

# %%
# Source Scrape URL 
    hemispheres_url = 'https://marshemispheres.com/'


# %%
# Retrieve page
    hemispheres_retrieve = requests.get(hemispheres_url)

# Create BeautifulSoup object
    hemi_soup = BeautifulSoup(hemispheres_retrieve.text, 'html.parser')

    hemispheres_html = browser.html
    hemispheres_results = BeautifulSoup(hemispheres_html, 'html.parser')


# %%
# Get URL of pages to be scraped
    url_results = hemi_soup.find_all('div', class_='item')
    url_list=[]

    for result in url_results:
        hemisphere=result.find('a')['href']
        url_list.append(hemisphere)

    print(url_list)

#%%
#Link Titles and image URLs
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "valles.html"},
        {"title": "Cerberus Hemisphere", "img_url": "cerberus.html"},
        {"title": "Schiaparelli Hemisphere", "img_url": "schiaparelli.html"},
        {"title": "Syrtis Major Hemisphere", "img_url": "syrtis.html"},
    ]

    mars_data = {
        "news_title": news_title,
        "news_sub_heading": news_teaser,
        "featured_image": featured_image_url,
        "mars_facts_table" : facts_html,
        "hemispheres_images": hemisphere_image_urls
    }

# %%
    browser.quit()
    
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.planetDB
    mars = db.mars
    db.mars.insert_one(mars_data)
    return mars_data

if __name__ == "__main__":
    mars = scrape()
    print(mars)
