#from flask import Flask
from bs4 import BeautifulSoup
import requests
import calendar
import psycopg2
from google_flight_analysis.scrape import Scrape, ScrapeObjects
#for flight web scraping go to this link.
#https://github.com/celebi-pkg/flight-analysis/tree/main

#app = Flask(__name__)

airports = ['ATL','DFW','DEN','ORD','LAX','JFK',
            'LAS','MCO','MIA','CLT','SEA','PHX',
            'EWR','SFO','IAH','BOS','FLL','MSP',
            'LGA','DTW']

weathersite = 'https://world-weather.info/forecast/usa/san_antonio/february-2024/'
heads = {'User-Agent': 'JBrigham/SPappas Traveling Foul project'}
weatherdata = requests.get(weathersite, headers = heads)
weathersoup = BeautifulSoup(weatherdata.text)
#BeautifulSoup.find all = soup.find("div", {"class":"locations-title ten-day-page-title"}).find("h1").text
days = weathersoup.findAll('li', {'class':['ww-month-weekdays forecast-statistics','ww-month-weekend forecast-statistics']}) #'ww-month-weekend forecast-statistics'
print(days)
print(days[0], '1')
print(days[1],'2')

x = 1
calendar.monthrange(2023,x)

orig_flight = 'PHX'#input('Enter Airport flying from')
dest_flight = 'LAX'#input('Enter airport flying to')

flight data = google_flight_analysis.scrape()







#@app.route("/")
#def hello_world():
#    return "<p>Hello, World!</p>"
    