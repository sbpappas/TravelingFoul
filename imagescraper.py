import bs4
import requests
from base64 import b64encode
import json
import shutil
import os
#os.chdir('data')
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import time

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome("chromedriver.exe")
driver.implicitly_wait(20)
driver.get(url)
#webscraper uses my provided username and authkey
#needs header with user-agent
def basic_auth(username, password):
     #allows account access by converting username and api to web header standards.
     token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
     return f'Basic {token}'

heads = {'User-Agent': 'Windows project', 'Authorization': basic_auth(user, api_key)}
flightreq = requests.get('kayak', headers=heads)
#makes it usable, as it gives us json back.
#pull posts, 
actualposts = usable['posts']
imgurls = []
#this pulls the actual post data out of the request
#its a list with each post stored as a dict sequentially.
#within each dict is a file entry that has the url we want.









