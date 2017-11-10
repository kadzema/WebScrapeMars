# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
import pandas as pd

def scrape():
        
    marsDict = {}    
    #### latest news title and article teaser from mars.nasa.gov
    url = 'https://mars.nasa.gov/news/'
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(url)
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='rollover_description_inner').text

    marsDict['news_title'] = news_title 
    marsDict['news_teaser'] = news_p
    print("News scraped")

    #### find the mars feature image
    # executable_path = {'executable_path': 'chromedriver'}
    # browser = Browser('chrome', **executable_path)
    imageurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    baseUrl = 'https://www.jpl.nasa.gov'
    browser.visit(imageurl)
    browser.click_link_by_partial_text('FULL IMAGE')
    imagehtml = browser.html
    imagesoup = BeautifulSoup(imagehtml, 'html.parser')
    more_info = imagesoup.find('a', class_='button fancybox').get('data-link')
    more_info = baseUrl + more_info
    browser.visit(more_info)
    moreinfohtml = browser.html
    moreinfosoup = BeautifulSoup(moreinfohtml, 'html.parser')
    figure = moreinfosoup.find('figure', class_='lede')
    featured_image_url = figure.find('a').get('href')
    featured_image_url = baseUrl + featured_image_url

    marsDict['featured_image_url'] = featured_image_url
    print("Featured image scraped")

    #### mars weather via twitter
    # executable_path = {'executable_path': 'chromedriver'}
    # browser = Browser('chrome', **executable_path)
    marsTwitterUrl = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(marsTwitterUrl)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    soup
    divs = soup.find_all('div', class_='content')
    for div in divs:
        try:
            yes = div.find('div', class_='stream-item-header').find('a').get('href')
            if yes == '/MarsWxReport':
                #we're in the right div, get the weather
                weather = div.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
                yes == ''
                # stop once we get the first/latest one
                break
        except Exception as e:
            pass

    marsDict['weather'] = weather
    print("Weather scraped")

    #### mars facts
    # executable_path = {'executable_path': 'chromedriver'}
    # browser = Browser('chrome', **executable_path)
    imageurl = 'https://space-facts.com/mars/'
    browser.visit(imageurl)
    soup = BeautifulSoup(browser.html,'html5lib')
    table = soup.find('table',class_="tablepress tablepress-id-mars") 
    df = pd.read_html(str(table))
    tableHTML = df[0].to_html(index=False, escape=True, header=None)
    tableHTML = tableHTML.replace('\n','')

    marsDict['factTable'] = tableHTML
    print("Fact table scraped")

    #### mars hemispheres
    # executable_path = {'executable_path': 'chromedriver'}
    # browser = Browser('chrome', **executable_path)
    hemispheresurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisphereBaseUrl = 'https://astrogeology.usgs.gov'
    browser.visit(hemispheresurl)
    soup = BeautifulSoup(browser.html,'html5lib')
    hemispheres = soup.find('div', class_='collapsible results').find_all('a')
    hemisphere_image_urls = []
    hemispheredict = {}

    for hemisphere in hemispheres:
        hemisphereLink = hemisphere.get('href')
        browser.visit(hemisphereBaseUrl + hemisphereLink)
        soup = BeautifulSoup(browser.html, 'html.parser')
        title = soup.find('title').text
        hemisphereTitle = title.split('|')
        hemisphereTitle = hemisphereTitle[0].replace(' Enhanced ','')
        imgUrl = soup.find('img',class_='wide-image').get('src')
        imgUrl = hemisphereBaseUrl + imgUrl
        hemispheredict = {"title": hemisphereTitle, "img_url":imgUrl}
        hemisphere_image_urls.append(hemispheredict)

    marsDict['HemisphereImages'] = hemisphere_image_urls
    print("Hemispheres scraped")
    print(marsDict)

    return(marsDict)

# print(scrape())