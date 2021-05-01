from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import time


dict_list = []
all_data = {}


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # visit mars news site
    mars_news_site_url = 'https://redplanetscience.com/'
    browser.visit(mars_news_site_url)

    mars_html = browser.html
    soup = bs(mars_html, 'html.parser')
    news_headline_list = soup.find_all('div', class_='content_title')
    news_text_list = soup.find_all('div', class_='article_teaser_body')
    news_headline = news_headline_list[0].text
    news_text = news_text_list[0].text 


    # Visit to Space Images
    mars_image_site_url = 'https://spaceimages-mars.com/'
    browser.visit(mars_image_site_url)
    mars_html = browser.html
    soup = bs(mars_html, 'html.parser')
    main_img_url = mars_image_site_url + soup.find('img', class_='headerimage fade-in').get('src')
    


    mars_facts_site_url = 'https://galaxyfacts-mars.com'
    browser.visit(mars_facts_site_url)

    mars_facts_html = browser.html
    soup = bs(mars_facts_html, 'html.parser')

    facts = pd.read_html(mars_facts_html)
    df1 = facts[0]
    header_row0 = 0
    df1.columns = df1.iloc[header_row0]
    df1.drop(header_row0, inplace=True)
    df1.set_index('Mars - Earth Comparison', inplace=True)

    df2 = facts[1]
    header_row1 = 0
    df2.columns = df2.iloc[header_row1]
    df2.drop(header_row1, inplace=True)
    df2.set_index('Equatorial Diameter:', inplace=True)


    # Hermisphere data
    mars_hemspheres_url = 'https://marshemispheres.com/'
    browser.visit(mars_hemspheres_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    links = soup.find_all('a', class_='itemLink product-item')


    for i in range(1, len(links),2):
        mydict= {}
        title = links[i].text.split('\n')[1]
        lnk = mars_hemspheres_url + links[i].get('href')
        browser.visit(lnk)
        html = browser.html
        soup = bs(html, 'html.parser')
        time.sleep(1)
        img_url = mars_hemspheres_url + soup.find('img', class_='wide-image').get('src')
        mydict['title'] = title
        mydict['link'] = lnk
        mydict['img_url'] = img_url
        dict_list.append(mydict)
        browser.back()

    browser.quit()
    all_data['main_image'] = main_img_url
    all_data['headlines'] = news_headline
    all_data['text'] = news_text
    all_data['hermisphere'] = dict_list
    all_data['facts'] = df1.to_dict('records')

    return all_data

            