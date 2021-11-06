from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_mars():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Visit each url
    url = "https://redplanetscience.com/"
    url1 = "https://spaceimages-mars.com/"
    url2 = "https://galaxyfacts-mars.com/"
    url3 = 'https://marshemispheres.com/'


    # Scrape page news into Soup
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    div = soup.find('div', {'class':'list_text'})
    title = div.find('div',{'class':'content_title'})
    article = div.find('div',{'class':'article_teaser_body'})

    # Get title and article paragrah
    news_title = title.text
    news_p = article.text

    # Scrape feature image
    browser.visit(url1)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    img = soup.find('img',{'class':'headerimage fade-in'})
    src = img['src']
    featured_image_url = url1+src

    # Scrape facts into pandas
    table = pd.read_html(url2)

    # Select mars facts table
    mars_df = table[0]
    mars_df = mars_df.rename(columns={0: 'Description', 1:'Mars', 2:'Earth'})
    # Convert to html
    mars_table = mars_df.to_html(index=False)
    mars_table_clean = mars_table.replace('\n', '')

    # Scrape Hemispheres Images
    browser.visit(url3)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    # Get images
    hemispheres = soup.find_all('div',{'class':'item'})
    hemisphere_image_url = []

    for hemisphere in hemispheres:
        hemisphere_dict = {}
    
        # Get title
        hemisphere_title = hemisphere.find('h3').text
        
        # Clicking link for each title to get image
        browser.links.find_by_partial_text(hemisphere_title).click()
        html = browser.html
        soup = bs(html, "html.parser")
        
        # Scrape image link
        hemis_div = soup.find('div', {'class':'wide-image-wrapper'})
        hemis_img = hemis_div.find('img',{'class':'wide-image'})['src']
        hemis_url = url3 + hemis_img
        
        # Fill dictionary
        hemisphere_dict['title'] = hemisphere_title
        hemisphere_dict['url'] = hemis_url
        
        # Append to list
        hemisphere_image_url.append(hemisphere_dict)
        
        #Set up browser to go back for each image
        browser.back()


    # Store data
    newsMars = {
        'news_title':news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_table':  mars_table_clean,
        'hemisphere_image_url': hemisphere_image_url
    }

    # Quit browser

    browser.quit()


    return newsMars
