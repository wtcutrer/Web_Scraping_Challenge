
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


# %%
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# %%
# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# %%
# Define database and collection
db = client.liftoff_db
collection = db.items

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


# %%
# Save file as html 
mars_html = facts_df.to_html('mars_table.html')
mars_html

# %% [markdown]
# ## Mars Hemishperes 

# %%
hemi_dict = []

# %% [markdown]
# ### Valles Marineris 

# %%
# Source Scrape URL 
hemi_url = 'https://marshemispheres.com/'
browser.visit(hemi_url)
time.sleep(3)


# %%
# Retrieve page
browser.links.find_by_partial_text('Valles Marineris').click()

hemi_html = browser.html
hemi_soup = BeautifulSoup(hemi_html, 'html.parser')


# %%
# Get URL of page to be scraped
img_link = hemi_soup.find('img', class_='wide-image').get('src')

#Pull Hemisphere title 
valles_title = hemi_soup.find('h2', class_='title').text

# Combine url & img link to make full html link=
valles_img = hemi_url + img_link

browser.back()

valles_dict = {'title:' + valles_title, 'img_url:' + valles_img}
hemi_dict.append(valles_dict)

valles_dict

# %% [markdown]
# ### Syrtis

# %%
# Source Scrape URL 
hemi_url = 'https://marshemispheres.com/'
browser.visit(hemi_url)
time.sleep(3)


# %%
# Retrieve page
browser.links.find_by_partial_text('Syrtis').click()

hemi_html = browser.html
hemi_soup = BeautifulSoup(hemi_html, 'html.parser')


# %%
# Get URL of page to be scraped
img_link = hemi_soup.find('img', class_='wide-image').get('src')

#Pull Hemisphere title 
syrt_title = hemi_soup.find('h2', class_='title').text

# Combine url & img link to make full html link=
syrt_img = hemi_url + img_link

browser.back()

syrt_dict = {'title:' + syrt_title, 'img_url:' + syrt_img}
hemi_dict.append(syrt_dict)

syrt_dict

# %% [markdown]
# ### Schiaparelli

# %%
# Source Scrape URL 
hemi_url = 'https://marshemispheres.com/'
browser.visit(hemi_url)
time.sleep(3)


# %%
# Retrieve page
browser.links.find_by_partial_text('Schiaparelli').click()

hemi_html = browser.html
hemi_soup = BeautifulSoup(hemi_html, 'html.parser')


# %%
# Get URL of page to be scraped
img_link = hemi_soup.find('img', class_='wide-image').get('src')

#Pull title 
schia_title = hemi_soup.find('h2', class_='title').text

# Get html link
schia_img = hemi_url + img_link

browser.back()

schia_dict = {'title:' + schia_title, 'img_url:' + schia_img}
hemi_dict.append(schia_dict)

schia_dict

# %% [markdown]
# ### Cerberus 

# %%
# Source Scrape URL 
hemi_url = 'https://marshemispheres.com/'
browser.visit(hemi_url)
time.sleep(3)


# %%
# Retrieve page
browser.links.find_by_partial_text('Cerberus').click()

hemi_html = browser.html
hemi_soup = BeautifulSoup(hemi_html, 'html.parser')


# %%
# Get URL of page to be scraped
img_link = hemi_soup.find('img', class_='wide-image').get('src')

#Pull title 
cerb_title = hemi_soup.find('h2', class_='title').text

# Get html link
cerb_img = hemi_url + img_link

browser.back()

cerb_dict = {'title:' + cerb_title, 'img_url:' + cerb_img}
hemi_dict.append(cerb_dict)

cerb_dict


# %%
print(hemi_dict)


# %%
browser.quit()


