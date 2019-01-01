import webbrowser
import time
import requests

api_key = 'AIzaSyCYjLqZeQa0ma3cKzaulANYmWvV8j5CQ9s'


def main():
    """
    @:return
    """
    # establishes start end and time data
    query_user()
    print(destination)
    print(origin)
    print(arrivalTime)
    # create link and queries service which outputs json
    json_total_routes = link_gen_and_query('filter routes')  # TODO: Steve, what is 'filter routes'?
    subway_stop_location = sort_routes(json_total_routes)
    arrival_time_transit = determine_arrival_time(subway_stop_location)
    launch_directions(arrival_time_transit, subway_stop_location)


def query_user():
    """
    Ask user for details about journey (destination, origin, Date, ETD), as invoked in
    main function
    @input: NONE
    @:return: reference to journey variables
    """
    global destination, origin, arrivalTime  # TODO: replace "global" with a pair?
    destination = input('What is the location of your event?').replace(" ","+")
    origin = input('Where will you be traveling from?').replace(" ","+")
    pattern = '%m.%d.%Y %H:%M'
    date_time = input('What day and time will the event be? Military Time(MM.DD.YYYY HH:MM)')
    arrivalTime = int(time.mktime(time.strptime(date_time, pattern)))


def link_gen_and_query(route_type):
    """
    Create Google Maps link based on the user input that can then generate a json for the journey.
    :param route_type: ?
    :return: json file
    """
    # generic start to every link
    start_link = "https://maps.googleapis.com/maps/api/directions''/json?"
    if route_type == 'all routes':
        # Specific end of link including API parameters
        end_link = "&mode=transit&transit_mode=subway&transit_mode=bus&alternatives=true"
        # Completion of link which includes  standard start stop and time data
        final_link = start_link + 'origin=%s&destination=%s&key=%s&arrival_time=%s'%(origin, destination, api_key, str(arrivalTime)) + end_link
        return requests.get(final_link).json()


def sort_routes(json):
    """
    Steve: what is the objective of this? Still to be developed based on original code?
    :param json: unused parameter
    :return:
    """
    middle_location = '711+Desplaines+Ave+Forest+Park+IL+60130'  # TODO: generalize this
    return middle_location


def determine_arrival_time(middleDestination):
    """
    Use route information within json and transfer "station" to understand when user will arrive at destination
    TODO: replace static buffer with an input from user (e.g. my mom needs 10 minutes, versus my dad 1 minute)
    :param middleDestination:
    :return: Arrive time (Military time)
    """
    StartLink = 'https://maps.googleapis.com/maps/api/directions''/json?'
    EndLink = '&mode=transit&transit_mode=subway'
    FinalLink = StartLink + 'origin=%s&destination=%s&key=%s&arrival_time=%s' % (origin, middleDestination, api_key, str(arrivalTime),) + EndLink
    jsonTotalRoutes = requests.get(FinalLink).json()
    buffer_time = 300  # number of seconds as buffer to required departure time to reach destination
    # Determines start time to get to destination and then adds buffer, this is in unix form
    arrivalTimeTransit = jsonTotalRoutes['routes'][0]['legs'][0]['departure_time']['value'] - buffer_time
    return arrivalTimeTransit


def launch_directions(aTT, sSL):
    startLink = 'https://www.google.com/maps/dir/?api=1&'
    drivinglink = startLink + 'origin=%s&destination=%s&travelmode=driving' % (origin, sSL)
    transitlink = startLink + 'origin=%s&destination=%s&travelmode=transit' % (sSL, destination)
    #this is the time 5 minutes before the estimated start time of the transit
    print(aTT)
    #Generates window but does not contain the correct time
    webbrowser.open(drivinglink)
    webbrowser.open(transitlink)

main()
