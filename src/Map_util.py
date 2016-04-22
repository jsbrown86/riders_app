'''
Map_Util.py
   
Author: Conor Tracey
Created:        April 21, 2016
Last Updated:   April 21, 2016
Contains functions to assist in making google maps in flask
Dependencies:
                flask_googlemaps flask extension
                    >>> pip3 install flask-googlemaps
'''

from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map


# To use one of these maps, go into the templates, and in the html
# file you want the map to appear in, between <head> and </head> type:
# {{name_of_map.js}}
# then type {{name_of_map.html}} where you want in in the page
#
# You will also need to render the map in the template_render function in flask
def make_map(pu_lat, pu_long, dr_lat, dr_long):
    '''
    (float, float) -> Map
    takes pickup lattitude/longitude and dropoff lattitude/longitude
    and returns a flask google map (for use in template rendering)
    with markers representing the pickup dropoff locations
    '''

    map = Map(
        identifier="view-side",
        zoom = 12,
        style = "height:450px;width:450px;margin:0;",
        lat=44.047705,
        lng=-123.086681,
        markers={'http://maps.google.com/mapfiles/ms/icons/green-dot.png':[(pu_lat,pu_long)],
                 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png':[(dr_lat, dr_long)]}
    )

    return map