# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/'
    browser.visit(url)

    time.sleep(1)

    # Create BeautifulSoup object; parse with 'html'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
 
    # results are returned as an iterable list
    results = soup.find_all('ul', class_="item_list list_view")
    #print(results)

        # Loop through returned results
    for result in results:
        # Error handling
        try:
        # Identify and return title of listing
            news_title = result.find('h3', class_="title").find('a').text
        
            link = result.a['href']
        
            final_link = 'https://mars.nasa.gov/' + link
        
            response_1 = requests.get(final_link)
        
            soup_1 = BeautifulSoup(response_1.text, 'html.parser')
        
            news_p = soup_1.find('div', class_="wysiwyg_content").p.text
        
        # Print results only if title, price, and link are available
            if (news_title and link):
                print('-------------')
                print(news_title)
                print(news_p)
                listings["headline"] = news_title
                listings["summary"] = news_p
        except AttributeError as e:
            print(e)
    
    # task 2
    url_1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_1)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # return image
    img = soup.find("div", class_="carousel_items").find("article")["style"].split("'")[1]
    featured_image_url = 'https://www.jpl.nasa.gov/' + img
    print(featured_image_url)
    listings["featured_image_url"] = featured_image_url

    # task 3
    url_2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results_tweets = soup.find_all("li", class_="js-stream-item stream-item stream-item ")
    #print(results_tweets)

    # Loop through returned results
    latest_mars_weather = []
    for tweets in results_tweets:
    # Error handling
        try:
        # Identify and return title of listing
            mars_weather = tweets.find("div", class_="js-tweet-text-container").text.strip()
            
        # Print results only if title, price, and link are available
            if 'Sol' in mars_weather:
                latest_mars_weather.append(mars_weather)
        except AttributeError as e:
            print(e)

    final_mars_weather = latest_mars_weather[0]
    listings["final_mars_weather"] = final_mars_weather

    # task 4
    url_3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_3)

    time.sleep(1)

    #tables
    df = tables[0]
    df.columns = ['Criteria', 'Values']
    #df.head()

    df.set_index('Criteria', inplace=True)
    #df.head()

    html_table = df.to_html()
    final_table = html_table.replace('\n', '')

    listings["final_table"] = final_table

    # task 5
    url_4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_4)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # results are returned as an iterable list
    results_1 = soup.find_all('div', class_="item")

    hemisphere_image_urls = []
    for result in results_1:
        #dict_hemisphere_image_urls = {}
        
        link = result.a['href']
        
        final_link = 'https://astrogeology.usgs.gov' + link
        
        response_1 = requests.get(final_link)
        
        soup_1 = BeautifulSoup(response_1.text, 'html.parser')
        
        title = soup_1.find('h2', class_="title").text
        
        img_url = soup_1.find('div', class_='downloads').find('a')['href']
        
        #dict_hemisphere_image_urls['title'] = title
                
        #dict_hemisphere_image_urls['img_url'] = img_url

        dictionary={"title":title,"img_url":img_url}

        hemisphere_image_urls.append(dictionary)

    print(hemisphere_image_urls)

    listings['hemisphere_image_urls'] = hemisphere_image_urls

    print(listings['hemisphere_image_urls'][0]['img_url'])

    
    return listings
