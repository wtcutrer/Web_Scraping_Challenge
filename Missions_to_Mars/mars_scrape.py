
# %% [markdown]
# # Stage 1 - Scraping Lift Off!

# %%
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo
import os
import pandas as pd
import time

def scrape():
# %%
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # %%
    mars= {}

    # %% [markdown]
    # ## NASA Mars News

    # %%
    # Source Scrape URL 
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    time.sleep(3)


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

    news_dict = {'news_title': news_title, 'news_summary': news_teaser}

    mars.update(news_dict)

    # %% [markdown]
    # ## JPL Mars Space Images - Featured Image

    # %%
    # Source Scrape URL 
    images_url = 'https://spaceimages-mars.com/'
    browser.visit(images_url)
    time.sleep(3)


    # %%
    # Retrieve page
    images_retrieve = requests.get(images_url)

    # Create BeautifulSoup object
    images_soup = BeautifulSoup(images_retrieve.text, 'html.parser')

    images_html = browser.html
    images_results = BeautifulSoup(images_html, 'html.parser')


    # %%
    # Retrieve Current Header Image from URL 
    featured_image = images_results.find('img', class_='headerimage')
    featured_image = featured_image['src']
    featured_image


    # %%
    #Combine URl and header image
    featured_image_url = images_url + featured_image
    print(featured_image_url)
    featured_image_url = {'featured_image': featured_image_url}
    mars.update(featured_image_url)

    # %% [markdown]
    # ## Mars Facts

    # %%
    # Source Scrape URL 
    facts_url = 'https://galaxyfacts-mars.com/'


    # %%
    #Set table data into Dataframe
    tables = pd.read_html(facts_url)
    facts_df = tables[0]
    facts_df.columns = ["Description","Mars_Data","Earth_Data"]
    facts_df.set_index("Description", inplace=True)
    facts_df


    # %%
    #Converted DataFrame into HTML string
    facts_html = facts_df.to_html()
    print(facts_html)


    # %%
    clean_html = facts_html.replace('\n', '')
    clean_html
    facts_dict={'mars_facts': clean_html}
    mars.update(facts_dict)


    # %%
    # Save file as html 
    mars_html = facts_df.to_html('mars_table.html')
    mars_html

    # %% [markdown]
    # ## Mars Hemishperes 

    # %%
    # URL of page to be scraped
    hemis_url = 'https://marshemispheres.com/'
    browser.visit(hemis_url)

    hemis_html = browser.html
    hemis_results = BeautifulSoup(hemis_html, 'html.parser')


    # %%
    # Get URL of pages to be scraped
    url_results = hemis_results.find_all('div', class_='item')

    url_list=[]

    for result in url_results:
        
        hemisphere=result.find('a')['href']
        url_list.append(hemisphere)


    print(url_list)


    # %%
    # Loop through URLs to scrape and get list of dictionaries
    hemisphere_image_urls=[]

    for item in url_list:
        item_url=hemis_url+item
        browser.visit(item_url)
        item_html=browser.html
        item_results=BeautifulSoup(item_html, 'html.parser')
        
        parent1=item_results.find('div', class_='cover')
        
        hemi_title=parent1.find('h2','title')
        hemi_title=hemi_title.text.strip()
        hemi_title=hemi_title.rstrip('Enhanced')
        hemi_title=hemi_title.rstrip(' ')
        
        parent2 = item_results.find('div', class_='downloads')
        first_image=parent2.find('ul')
        hemi_image_item = first_image.find_all('li')[0]
        hemi_image = hemi_image_item.find('a')['href']
        
        hemisphere_image_url={"title": hemi_title, "image_url": hemis_url+hemi_image}
        hemisphere_image_urls.append(hemisphere_image_url)


    # %%
    #Update mars dictionary
    mars.update({'hemispheres':hemisphere_image_urls})

    print(hemisphere_image_urls)


    # %%
    print(mars)


    # %%
    browser.quit()

    return mars

if __name__ == "__main__":
    scrape_info = scrape()
    print(scrape_info)


# %% [markdown]
# # Store Results in Mongo 

# %%
# Initialize PyMongo to work with MongoDBs
# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)


# # %%
# # Define database and collection
# db = client.mars_db
# collection = db.mars_info


# %%
# collection.insert_one(mars)


