import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs

source_urls = {
    'news' : 'https://mars.nasa.gov/news/',
    'featured_images' : 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars',
    'weather' : 'https://twitter.com/marswxreport?lang=en',
    'facts' : 'http://space-facts.com/mars/',
    'hemispheres': 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
}

def retrieve_news():
    browser = Browser("chrome",headless=True)
    browser.visit(source_urls['news'])
    soup = bs(browser.html, 'html.parser')

    slides = soup.body.find_all('li',class_='slide')
    articles = []
    for slide in slides:
        title = slide.h3.text
        teaser = slide.find_all('div',class_='article_teaser_body')[0].text
        articles.append({'title' : title, 'description' : teaser})

    news_title = articles[0]['title']
    news_p = articles[0]['description']
    return news_title, news_p

def retrieve_featured_img():
    browser = Browser("chrome",headless=True)
    browser.visit(source_urls['featured_images'])
    soup = bs(browser.html, 'html.parser')

    JPLURL = 'https://www.jpl.nasa.gov'
    slides = soup.find_all('li',class_='slide')
    featured_images = []
    for slide in slides:
        try:
            featured_images.append(JPLURL + slide.a['data-fancybox-href'])
        except KeyError:
            pass

    featured_image_url = featured_images[0]
    return featured_image_url

def retrieve_weather():
    browser = Browser("chrome",headless=True)
    browser.visit(source_urls['weather'])
    soup = bs(browser.html, 'html.parser')

    mars_username = '@MarsWxReport'
    tweets = soup.body.find_all('div',class_='tweet')
    mars_posts = []
    for tweet in tweets:
        if tweet.find_all('span',class_='username')[0].text == mars_username:
            mars_posts.append(tweet.find_all('p',class_='tweet-text')[0].text)

    mars_weather = mars_posts[0]
    return mars_weather

def retrieve_facts():
    browser = Browser("chrome",headless=True)
    browser.visit(source_urls['facts'])
    mars_facts_df = pd.read_html(browser.html)[0]
    table_string = mars_facts_df.to_html()
    return table_string

def retrieve_hemispheres():
    browser = Browser("chrome",headless=True)
    browser.visit(source_urls['hemispheres'])
    browser.click_link_by_partial_text('Enhanced')

    browser.click_link_by_partial_text('Back')

    hemisphere_links = browser.find_link_by_partial_text('Hemisphere')
    link_text = []
    for link in hemisphere_links:
        link_text.append(link.text)
    hemisphere_image_urls = []
    for link in link_text:
        browser.click_link_by_partial_text(link)
        hemisphere_image_urls.append({
            'title' : link[:-9],
            'tif_url' : browser.find_link_by_partial_text('Original')['href'],
            'jpg_url' : browser.find_link_by_text('Sample')['href'],
        })
        browser.click_link_by_partial_text('Back')
    return hemisphere_image_urls

def scrape():
    browser = Browser("chrome",headless=True)
    (news_title, news_p) = retrieve_news()
    content = {
        'latest_news' : {
            'title' : news_title,
            'description' : news_p
        },
        'featured_image' : retrieve_featured_img(),
        'weather' : retrieve_weather(),
        'facts' : retrieve_facts(),
        'hemispheres' : retrieve_hemispheres() 
    }
    return content