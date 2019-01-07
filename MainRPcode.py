import webbrowser
import time
import requests

api_key = 'AIzaSyB23T32B3CyuMJNUD30OA-V7qfCeL8GcUE'


def main():
    """
    main function which will execute all other functions in program to perform task
    :input: none
    :return: Generate two web pages (directions to CTA, directions to destination from CTA)
    """
    # establishes start end and time data
    query_user()
    # returns optimal subway stop
    subway_stop_location = sort_routes()
    # returns the time you need to arrive at the CTA
    arrival_time_transit = determine_arrival_time(subway_stop_location)
    # launches directions in google maps, with two windows for directions to and from CTA
    launch_directions(arrival_time_transit, subway_stop_location)


def query_user():
    """
    query_user() function has pre-assigned variables above for testing purposes
    :input: none
    :return:
    """

    global destination, origin, arrival_time

    arrival_time = 1547235000
    origin = '41.720055,-87.751211'
    destination = 'grant park chicago il'

    """
    destination = input('What is the location of your event?').replace(" ","+")
    origin = input('Where will you be traveling from?').replace(" ","+")
    pattern = '%m.%d.%Y %H:%M'
    date_time = input('What day and time will the event be? Military Time(MM.DD.YYYY HH:MM)')
    arrival_time = int(time.mktime(time.strptime(date_time, pattern)))
    """


def sort_routes():
    """

    :return: an array of the closest subway stops by distance (miles)
    """

    subway_stop_candidates = nearby_search_request(origin)
    # next three lines put lat long coordinates into lat,long|lat,long|lat,long... as standard
    # in the  documentation for the link
    # (see API doc. https://developers.google.com/maps/documentation/distance-matrix/intro)
    bar_list_format_candidates = ''
    for x in subway_stop_candidates:
        bar_list_format_candidates = bar_list_format_candidates + x + '|'
    # TODO the rest of this function block is the main thing to finish to make functional, you need to
    # TODO determine the best CTA stop using distance matrix, this partially code already, function returns CTA stop
    start_link = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    parameters = 'origins=%s&destinations=%s&key=%s' % (origin, bar_list_format_candidates, api_key)
    final_link = start_link + parameters
    json = requests.get(final_link).json()
    # json['rows'][]
    webbrowser.open(final_link)

    '''
    for x in subway_stop_candidates:
        start_link = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        parameters_drive = 'origins=%s&destinations=%s&key=%s'%(origin,x,api_key)
        parameters_transit = '&origins=%s&destinations=%s&key=%s'%(x,destination,api_key)
    '''
    # TODO: FYI Steve I commented the below line, which was returning an error
    # return subway_location


def determine_arrival_time(middle_destination):
    """
    Function determines what time the user must arrive in order to catch their train
    :param middle_destination: mode transfer station; this will eventually need to be computed
    :return:
    """

    start_link = 'https://maps.googleapis.com/maps/api/directions''/json?'
    end_link = '&mode=transit&transit_mode=subway'
    final_link = start_link + 'origin=%s&destination=%s&key=%s&arrival_time=%s' % (
    origin, middle_destination, api_key, str(arrivalTime),) + end_link
    # change to directions matrix
    json_total_routes = requests.get(final_link).json()
    # determines start time to get to destination and then adds 5 minute (300 sec) buffer, this is in unix form
    buffer_time = 300
    arrival_time_transit = json_total_routes['routes'][0]['legs'][0]['departure_time']['value'] - buffer_time
    return arrival_time_transit


def launch_directions(arrival_time_transit, subway_stop_location):
    """
    Function will launch the directions for the most preferred path
    :param arrival_time_transit:
    :param subway_stop_location:
    :return:
    """
    # API for web browser generation https://developers.google.com/maps/documentation/urls/guide
    start_link = 'https://www.google.com/maps/dir/?api=1&'
    driving_link = start_link + 'origin=%s&destination=%s&travelmode=driving' % (origin, subway_stop_location)
    transit_link = start_link + 'origin=%s&destination=%s&travelmode=transit' % (subway_stop_location, destination)
    # this is the time 5 minutes before the estimated start time of the transit
    # currently not able to input in web browser (yes so its useless at the moment)
    print(arrival_time_transit)
    # generates window but does not contain the correct time
    webbrowser.open(driving_link)
    webbrowser.open(transit_link)


def nearby_search_request(location):
    """
    Documentation for API @ https://developers.google.com/places/web-service/search
    :param location:
    :return:
    """
    start_link = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    # (straight from documentation) A term to be matched against all content that Google has indexed for this place
    # including but not limited to name, type, and address, as well as customer reviews and other third-party content.
    keyword = 'CTA'
    # consider using name instead?
    # this is the area to be searched which must be specified in lat/long
    transit_type = 'subway_station'
    parameters = 'key=%s&location=%s&keyword=%s&type=%s&rankby=distance' % (api_key, location, keyword, transit_type)
    final_link = start_link + parameters
    # print (final_link)
    # webbrowser.open(final_link)
    json = requests.get(final_link).json()
    lat_long_array = []
    for x in json['results']:
        lat_long_array.append(str(x["geometry"]["location"]['lat']) + ',' + str(x["geometry"]["location"]['lng']))
        # consider breaking after say 5 iterations? aka only check top 5
        break
    return lat_long_array


main()
