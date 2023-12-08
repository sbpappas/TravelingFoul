from flask import Flask, request
import hello
api = Flask(__name__)

@api.route('/profile')
def my_profile():
    response_body = {
        "name": "Test",
    }
    return response_body

@api.route('/flightreq', methods=['POST'])
def request_flight():
    data = request.get_json()
    orig = data['orig']
    dest = data['dest']
    startdate = data['startdate']
    enddate = data['enddate']
    flight = hello.flight_search(orig,dest,startdate,enddate)
    print(flight,'found flight')
    resp = {
        'flight': flight
    }
    return resp
    
