# Dependencies
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint
import pymongo
from flask import Flask, render_template
import time
import numpy as np
import json
from selenium import webdriver

# Create an instance of Flask
app = Flask(__name__)

def scrape_all():
    # splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_p = mars_news(browser)
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": mars_features_image(browser),
        "Mars_facts_table": mars_table(),
        "hemispheres": mars_hemispheres(browser)
    }
    browser.quit()
    return mars_data



def mars_news(browser):
    url1 = "https://redplanetscience.com/"
    browser.visit(url1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div',class_='content_title').text
    news_p = soup.find('div',class_='article_teaser_body').text
    return news_title, news_p

def mars_features_image(browser):
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.findAll('img', class_="headerimage fade-in")
    for image in images:
        print (image['src'])
    image_url = "image/featured/mars1.jpg"
    featured_image_url = url + image_url
    return featured_image_url


def mars_table():
    url2 = "https://galaxyfacts-mars.com/"
    fact_table=pd.read_html(url2)
    df = fact_table[0]
    df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']
    html_table = df.to_html()
    return html_table


def mars_hemispheres(browser):
    url3 = "https://marshemispheres.com/"
    browser.visit(url3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_urls=[]
    for i in range(4):
        hemisphere_dict = {}
        browser.find_by_css("a.product-item img")[i].click()
        sample = browser.find_by_text("Sample").first
        hemisphere_dict["img_url"]=sample["href"]
        hemisphere_dict["title"]=browser.find_by_css("h2.title").text
        hemisphere_urls.append(hemisphere_dict)
        browser.back()
    return hemisphere_urls


if __name__ == "__main__":
    print(scrape_all())