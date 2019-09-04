# Code to Get Co-Ordinates
import math
import requests
import operator

def get_cords(my_lat,my_long,dist,angle):
    
    """The function get_cords() returns the user defined latitude and longitude coordinates in degrees"""
    
    R = 3963.167 #Radius of the Earth in miles
    brng = math.radians(angle) #Bearing is converted to radians.
    d = dist #Distance in miles
    lat1 = math.radians(my_lat) #Current lat point converted to radians
    lon1 = math.radians(my_long) #Current long point converted to radians
    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return(lat2,lon2)

#Code to Get Extents of Map Range within our mile radius
def get_extent(my_lat,my_long,dist):
    
    """This function intends to calculate the latitude and longitude range in which the airports will be located. 
       The 3 angles were assumed on the basis of the understanding that the user is in the middle of a rectangle 
       (inside a circle) and to calculate the extent of latitude and longitude, we would require coordinates on 
       the 3 edges which makes the 3 respective angles with the center: 45, -45 and -135"""
    
    top_left=get_cords(my_lat,my_long,dist,-45)
    bot_left=get_cords(my_lat,my_long,dist,-135)
    top_right=get_cords(my_lat,my_long,dist,45)
    lat_range=[bot_left[0],top_left[0]]
    long_range=[top_left[1],top_right[1]]
    return(lat_range,long_range)

def test_sorted_airport(my_loclat,my_loclong,myrange):
    
    """This function returns the list of airports in the vicinity of the user provided location coordinates,
    sorted on the basis of their distance from the user. The limit of displayed airports have been increased
    to 200 instead of the default 25. This function also takes care of the case in which the airport's distance 
    from the user falls outs of the given range - for which their would be no output"""
    
    lat_range,long_range=get_extent(my_loclat,my_loclong,myrange)
    url="https://mikerhodes.cloudant.com/airportdb/_design/view1/_search/geo?q=lat:["+str(lat_range[0])+"00%20TO%20"+str(lat_range[1])+"]%20AND%20lon:["+str(long_range[0])+"%20TO%20+"+str(long_range[1])+"]&sort=%22%3Cdistance,lon,lat,"+str(my_loclong)+","+str(my_loclat)+",mi%3E%22&limit=200"
    my_result=[]
    r = requests.get(url)
    for i in r.json()['rows']:
        airport_name=(i['fields']['name'])
        dist=(i['order'][0])
        if(dist>myrange):
            break
        else:
            my_result.append(str('Airport: ' + airport_name+', Distance From Location = '+str(dist)))
    return(my_result)

def main():
    mlat=input("Enter Your Location Latitude = ")
    mlong=input("Enter Your Location Longitude = ")
    mdist=input("Enter Your Distance Range for Airports in Miles = ")
    print(sorted_airport(mlat,mlong,mdist))
if __name__== "__main__":
  main()
