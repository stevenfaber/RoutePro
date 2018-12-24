import webbrowser
import time
import requests

api_key = 'AIzaSyCYjLqZeQa0ma3cKzaulANYmWvV8j5CQ9s'

string destination, origin;
int time;

def main():

    #establishes start end and time data
    queryUser()
    #create link for json query using function
    api_link = linkGenAndQuery('filter routes')
    #uses link in prior line and generates json which is later manipulated
    jsonTotalRoutes = requests.get(api_link).json()
    subwayStopLocation = sortRoutes(jsonTotalRoutes)
    arrivalTimeTransit = determineArrivalTime(subwayStopLocation)
    launchDirections(arrivalTimeTransit,subwayStopLocation)


def queryUser():
    global destination = raw_input('What is the location of your event?').replace(" ","+")
    global origin = raw_input('Where will you be traveling from?').replace(" ","+")
    pattern = '%m.%d.%Y %H:%M'
    date_time = raw_input('What day and time will the event be? Militaty Time(MM.DD.YYYY HH:MM)')
    global time = int(time.mktime(time.strptime(date_time, pattern)))


def linkGenAndQuery(routeType):
    #generic start to every link
    StartLink = 'https://maps.googleapis.com/maps/api/directions''/json?'
    if(routeType = 'filter routes'){
    #Specific end of link including API parameters
    EndLink = '&mode=transit&transit_mode=subway&transit_mode=bus&alternatives=true'
    #Completion of link which includes  standard start stop and time data
    FinalLink = StartLink + 'origin=%s&destination=%s&key=%s&arrival_time=%s'%(origin,destination,api_key,str(time),) + EndLink
    return FinalLink
    }
    EndLink = '&mode=transit&transit_mode=subway'
    FinalLink = StartLink + 'origin=%s&destination=%s&key=%s&arrival_time=%s'%(origin,destination,api_key,str(time),) + EndLink
def sortRoutes(json):
    return middle location
def determineArrivalTime():
    StartLink = 'https://maps.googleapis.com/maps/api/directions''/json?'
    EndLink = '&mode=transit&transit_mode=subway'
    FinalLink = StartLink + 'origin=%s&destination=%s&key=%s&arrival_time=%s' % (origin, destination, api_key, str(time),) + EndLink
    jsonTotalRoutes = requests.get(FinalLink).json()
    #Determines start time to get to destination and then adds 5 minute (300 sec) buffer, this is in unix form
    arrivalTimeTransit = jsonTotalRoutes['routes'][0]['legs'][0]['departure_time']['value'] - 300
    return arrivalTimeTransit
def launchDirections(aTT,sSL)
    startLink = 'https://www.google.com/maps/dir/?api=1&''
    drivinglink = starLink + 'origin=%s&destination=%s&travelmode=driving' % (origin, sSL)
    transitlink = starLink + 'origin=%s&destination=%s&travelmode=transit' % (sSL, destination)
    #this is the time 5 minutes before the estimated start time of the transit
    print(aTT)
    #Generates window but does not contain the correct time
    webbrowser.open(drivinglink)
    webbrowser.open(transitlink)
main()