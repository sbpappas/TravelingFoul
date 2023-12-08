#from flask import Flask
from bs4 import BeautifulSoup
import requests
import calendar
import psycopg2
import pandas
from google_flight_analysis.scrape import Scrape, ScrapeObjects
#https://github.com/celebi-pkg/flight-analysis/tree/main
#connect to database
conn = psycopg2.connect('dbname=postgres user=postgres password=spappas')
cursor = conn.cursor()
airports = ['ATL','DFW','DEN','ORD','LAX','JFK',
            'LAS','MCO','MIA','CLT','SEA','PHX',
            'EWR','SFO','IAH','BOS','FLL','MSP',
            'LGA','DTW']
airportconvert = {'ATL':"atlanta_1",'DFW':"dallas_1","DEN":'denver','ORD':'chicago','LAX':'los_angeles','JFK':"new_york",
            'LAS':'las_vegas_1','MCO':'orlando','MIA':'miami','CLT':'charlotte','SEA':'seattle','PHX':'phoenix',
            'EWR':'newark_1','SFO':'san_jose','IAH':'houston_11','BOS':'boston','FLL':'fort_lauderdale','MSP':'minneapolis',
            'LGA':'new_york','DTW':'detroit', 'SAT':'san_antonio'}
month_dict = {
    1: 'january',
    2: 'february',
    3: 'march',
    4: 'april',
    5: 'may',
    6: 'june',
    7: 'july',
    8: 'august',
    9: 'september',
    10: 'october',
    11: 'november',
    12: 'december'
}
weatherdescriptions = ['Clear sky','Few clouds','Partly cloudy','Broken clouds','Overcast clouds','Light rain',
                        'Light intensity drizzle','Heavy intensity rain','Drizzle','Snow','Rain and snow','Light intensity shower rain']
goodweather = ['Clear sky','Few clouds','Partly cloudy','Broken Clouds']
#find flight on each date, find weather on each date, throw all in database...
#city = input("enter destination airport code").upper()
#origdate = input('enter date in form "yyyy-mm-dd"')

def scrapeweather(date, orig_flight, dest_flight):
    date  = date.split('-')
    day = int(date[2])
    month = int(date[1])
    year = date[0]
    weathersite = 'https://world-weather.info/forecast/usa/san_antonio/february-2024/'
    changedsite = f'https://world-weather.info/forecast/usa/{airportconvert[orig_flight]}/{month_dict[month]}-{year}'
    heads = {'User-Agent': 'JBrigham/SPappas Traveling Foul project'}
    weatherdata = requests.get(changedsite, headers = heads)
    weathersoup = BeautifulSoup(weatherdata.text,features='html.parser')
    days = weathersoup.findAll('li', {'class':['ww-month-weekdays forecast-statistics','ww-month-weekend forecast-statistics','ww-month-weekend foreacast','ww-month-weekdays foreacast']}) #'ww-month-weekend forecast-statistics'
    #print(days, 'days',changedsite, 'changedsite',day,'day')
    for _ in days:
        if _.find('div').text == str(day): #list of weather data is given as tags, have to call find on them to unwrap and text to actually get the day number out
            dateweather = _
    #dateweather = days.find([day-1] #weather on date of arrival at destination airport
    #print(days)
#wea    ther description, high, low
    print(dateweather)
    hitemp = dateweather.findChild('span').text
    hitemp = ''.join(c for c in hitemp if c.isdigit())
    lotemp = dateweather.findChild('p').text
    lotemp = ''.join(c for c in lotemp if c.isdigit())
    dateInfo = [dateweather.findChild('i')['title'],hitemp, lotemp]
    #weatherinsert(orig_flight,dateInfo, origdate)
    #print(dateInfo,'weather on that day')
    return dateInfo
#flight id (primary key), destination, origin, price, departure date time, arrival date time, airline

#weatherid (key), location (same as flight destination), temp_hi, temp_lo, description, date 
def scrapeflight(date, orig_flight, dest_flight):
    '''scraping flight data here'''
    results = Scrape(orig_flight, dest_flight, date)
    ScrapeObjects(results) #scrapeobjects changes results in place
    flightdata = results.data
    row = flightdata['Price ($)'].idxmin()
    flight = flightdata.iloc[row]
    #print(type(flight))
    #print(flight)
    arrivedate = str(flight['Arrival datetime'])
    arrivedate = arrivedate.split(' ')
    arrivedate = arrivedate[0]
    departuredate =  str(flight['Departure datetime'])
    departuredate = departuredate.split(' ')
    departuredate = departuredate[0]
    return [int(flight['Price ($)']), departuredate, arrivedate, str(flight['Airline(s)'])]

    #return flight

    #print(flightdata['Price ($)'].min())
    #print(flightdata['Price ($)'].max())
    # REF FLIGHTS
    # SFO- LAX 2024-02-02 2024-02-04
    # LAX - PHX 2023-12-30 2023-12-31
    # ATL- IAH  2024-03-01 2024-03-03
    # option 2: SFO
    # (BAD WEATHER example flight:)
#calendar.monthrange(2023,x)
#postgresql port num is 5432, superuser password is spappas
#db commands

#CREATE TABLE weather (weatherid SERIAL PRIMARY KEY, dest VARCHAR(3), temp_hi INTEGER,
#  temp_lo INTEGER, description VARCHAR(50), date VARCHAR(20));

def weatherinsert(dest_city, dateInfo, origdate):
    cursor.execute("""
         INSERT INTO weather (dest, temp_hi, temp_lo, description, date)
        VALUES (%s, %s, %s,%s,%s);
        """,
        (dest_city, dateInfo[1], dateInfo[2], dateInfo[0], origdate))
    
def flightinsert(dest_city, orig_city, dateInfo):
    cursor.execute("""
        INSERT INTO flights (dest, orig, price, depart_time, arrive_time, airline)
        VALUES (%s, %s, %s, %s, %s,%s);
        """,
        (dest_city, orig_city, dateInfo[0], dateInfo[1], dateInfo[2], dateInfo[3]))
def flight_search(orig,dest,startdate,enddate):
        cursor.execute('''INSERT INTO userpref (city) VALUES (%s)''', (dest,)) #the comma is required you must provide a tuple...
        daterange = pandas.date_range(start=startdate,end=enddate)
        print('Finding cheapest flights and best weather for all dates.')
        for _ in daterange:
            flightdate = str(_).split(' ')[0]
            dateinfo = scrapeweather(flightdate,orig, dest)
            weatherinsert(dest, dateinfo, flightdate)
            flightinfo = scrapeflight(flightdate,orig, dest)
            flightinsert(dest, orig, flightinfo )
        cursor.execute("SELECT * from weather WHERE (description = 'Clear sky' or description = 'Few Clouds') and dest = (%s) and date = (%s);",(dest,enddate))
        goodday = cursor.fetchone()
        if goodday == None:
            print('No good weather...')
            return('none')
        else:
            date = str(goodday[5])
            print(date)
            cursor.execute("SELECT * from flights WHERE arrive_time = (%s) and dest = (%s) and orig = (%s);",(date,dest,orig))
            bestflight = cursor.fetchone()
            #print(bestflight)
            if bestflight == None:
                print('No flights were available on that day...')
                return('none')
            else:
                print("Best Flight info: ", bestflight)
                return(bestflight)
        conn.commit()
        conn.close()
#CREATE TABLE flights (flightid SERIAL PRIMARY KEY, dest VARCHAR(3), orig VARCHAR(3), 
# price INTEGER, depart_time VARCHAR(50), arrive_time VARCHAR(50), airline VARCHAR(50));
if __name__ == '__main__':
    choice= input('Enter flight search mode: 1 = Normal, 2 = recommendation')
    if choice == '2':
        cursor.execute("SELECT mode() WITHIN GROUP (ORDER BY city) as best from userpref;")
        best = cursor.fetchone()
        print(f"The oracle has chosen {best[0]} as your destination.")
        print('Finding flight for you...')
        date = "2024-04-01"
        orig_city = input('Enter airport code of where you would like to fly out of.').upper()
        flightinfo = scrapeflight(date,orig_city, best[0])
        print(flightinfo)
        print('Flight is: ', flightinfo)
        conn.commit()
        conn.close()
    else:
        orig_city = input("enter origin airport code ").upper() #'PHX' #
        dest_city = input("enter destination airport code ").upper() #'SAT' #
        
        startdate = input('Enter first date of range in form "yyyy-mm-dd" ')# '2024-01-01' #input
        enddate = input('Enter end date of range in form "yyyy-mm-dd" ') #2024-01-03' #
        flight_search(orig_city,dest_city,startdate,enddate)




#cursor.execute("INSERT INTO example (num) VALUES (100);")
#print('threw into database')
#cursor.execute("SELECT * FROM example;")
#cursor.fetchone()

#result = Scrape('JFK', 'IST', '2024-08-20')
#ScrapeObjects(result)
#fullrest = result.data.to_string() #see data


#@app.route("/")
#def hello_world():
#    return "<p>Hello, World!</p>"
    