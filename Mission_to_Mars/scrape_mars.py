from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():

    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)   

def scrape():

    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find("li", class_="slide").find("div", class_="content_title").text
    news_p = soup.find("li", class_="slide").find("div", class_="article_teaser_body").text

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')
    
    image_name = soup.find('article', class_='carousel_item')['alt']

    base_url = "https://www.jpl.nasa.gov"
    img_src = soup.find(attrs={'data-title':image_name})["data-fancybox-href"]

    featured_image_url = base_url + img_src

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(5)
    
    html = browser.html
    soup = bs(html, 'html.parser')

    tweets = soup.find_all("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

    for tweet in tweets:
        if "InSight" in tweet.find("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text:
            mars_weather = tweet.find("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text
            break

    url = "https://www.space-facts.com/mars"
    browser.visit(url)
    html = browser.html
    data = pd.read_html(html)

    mars_facts_df = data[0]
    mars_facts_df.columns = ["Property", "Value"]
    mars_facts_df

    html_table = mars_facts_df.to_html()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    links = soup.find_all("div", class_="item")

    hemisphere_image_urls = []

    for link in links:
        end_point = link.find("a")["href"]
        url = "https://astrogeology.usgs.gov" + end_point
        browser.visit(url)
        html = browser.html
        soup = bs(html, "html.parser")
    
        title = soup.find("div", class_="content").find("h2").text
        img_url = soup.find("div", class_="downloads").find("a")["href"]
    
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    mars_info = {
        "News_Title": news_title,
        "Paragraph_Text": news_p,
        "Most_Recent_Mars_Image": featured_image_url,
        "Mars_Weather": mars_weather,
        "Mars_Table": html_table,
        "Mars_Hemispheres": hemisphere_image_urls
    }

    browser.quit()

    return mars_info