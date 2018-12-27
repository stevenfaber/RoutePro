import webbrowser
import time
import requests

api_key = 'AIzaSyCYjLqZeQa0ma3cKzaulANYmWvV8j5CQ9s'


def main():

    #establishes start end and time data
    queryUser()
    print (destination)
    print (origin)
    print (arrivalTime)
    #create link and queries service which outputs json
    jsonTotalRoutes = linkGenAndQuery('filter routes')
    subwayStopLocation = sortRoutes(jsonTotalRoutes)
    arrivalTimeTransit = determineArrivalTime(subwayStopLocation)
    launchDirections(arrivalTimeTransit,subwayStopLocation)


def queryUser():
    global destination, origin, arrivalTime
    destination = input('What is the location of your event?').replace(" ","+")
    origin = input('Where will you be traveling from?').replace(" ","+")
    pattern = '%m.%d.%Y %H:%M'
    date_time = input('What day and time will the event be? Militaty Time(MM.DD.YYYY HH:MM)')
    arrivalTime = int(time.mktime(time.strptime(date_time, pattern)))


def linkGenAndQuery(routeType):
    #generic start to every link
    StartLink = "https://maps.googleapis.com/maps/api/directions''/json?"
    if(routeType == 'all routes'):
        #Specific end of link including API parameters
        endLink = "&mode=transit&transit_mode=subway&transit_mode=bus&alternatives=true"
        #Completion of link which includes  standard start stop and time data
        finalLink = StartLink + 'origin=%s&destination=%s&key=%s&arrival_time=%s'%(origin, destination, api_key, str(arrivalTime)) + endLink
        return requests.get(finalLink).json()


def sortRoutes(json):
    middle_location = '711+Desplaines+Ave+Forest+Park+IL+60130'
    return middle_location

def determineArrivalTime(middleDestination):
    StartLink = 'https://maps.googleapis.com/maps/api/directions''/json?'
    EndLink = '&mode=transit&transit_mode=subway'
    FinalLink = StartLink + 'origin=%s&destination=%s&key=%s&arrival_time=%s' % (origin, middleDestination, api_key, str(arrivalTime),) + EndLink
    jsonTotalRoutes = requests.get(FinalLink).json()
    #Determines start time to get to destination and then adds 5 minute (300 sec) buffer, this is in unix form
    arrivalTimeTransit = jsonTotalRoutes['routes'][0]['legs'][0]['departure_time']['value'] - 300
    return arrivalTimeTransit

def launchDirections(aTT,sSL):
    startLink = 'https://www.google.com/maps/dir/?api=1&'
    drivinglink = startLink + 'origin=%s&destination=%s&travelmode=driving' % (origin, sSL)
    transitlink = startLink + 'origin=%s&destination=%s&travelmode=transit' % (sSL, destination)
    #this is the time 5 minutes before the estimated start time of the transit
    print(aTT)
    #Generates window but does not contain the correct time
    webbrowser.open(drivinglink)
    webbrowser.open(transitlink)

main()
