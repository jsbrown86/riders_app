"""
Input_Validation.py

Author:       Conor Tracey

Created:      Apr 17, 2016
Last Updated: Apr 20, 2016

Dependencies: geopy (python geocoding extension)
                  >>> pip3 install geopy

This module contains functions that allow checking if a particular address
falls within the Safe Ride Boundaries. 

"""

from geopy.geocoders import Nominatim


#Global Array for storing abstracted Safe Ride boundary
#Each element in BOUNDARIES is stored in the form:
#   [N(lat), S(lat), E(long), W(long)]                          Reg
BOUNDARIES = [[44.029945, 44.028138, -123.131946, -123.135052], #0
              [44.030089, 44.028394, -123.129543, -123.131946], #1
              [44.030455, 44.028394, -123.128449, -123.129543], #2
              [44.048475, 44.028262, -123.126271, -123.128449], #3
              [44.048475, 44.027954, -123.125843, -123.126271], #4
              [44.048475, 44.027627, -123.125373, -123.125843], #5
              [44.048475, 44.027347, -123.124944, -123.125373], #6
              [44.048475, 44.027004, -123.123860, -123.124944], #7
              [44.052598, 44.026803, -123.119131, -123.123860], #8
              [44.064272, 44.026803, -123.118211, -123.119131], #9
              [44.064272, 44.014397, -123.112883, -123.118211], #10
              [44.071475, 44.014960, -123.107050, -123.112883], #11
              [44.071151, 44.017656, -123.105518, -123.107050], #12
              [44.070848, 44.017656, -123.104733, -123.105518], #13
              [44.070486, 44.017367, -123.100923, -123.104733], #14
              [44.078023, 44.017367, -123.093001, -123.100923], #15
              [44.078023, 44.011229, -123.074291, -123.093001], #16
              [44.078023, 44.011831, -123.072891, -123.074291], #17
              [44.078023, 44.012174, -123.071582, -123.072891], #18
              [44.078023, 44.024044, -123.068691, -123.071582], #19
              [44.070248, 44.024044, -123.061174, -123.068691], #20
              [44.070248, 44.026729, -123.059713, -123.061174], #21
              [44.070248, 44.028437, -123.053351, -123.059713], #22
              [44.070248, 44.028828, -123.051348, -123.053351], #23
              [44.070248, 44.030968, -123.049338, -123.051348], #24
              [44.069958, 44.040070, -123.047658, -123.049338], #25
              [44.077423, 44.069958, -123.041699, -123.047658]  #26
    ]


def Address_to_Long_Lat(address):
    '''
    (string) -> tuple

    This function uses the geopy extension to convert address strings to
    Latitude Longitude coordinates. It returns these coordinates in the form
    of a tuple with (latitude, longitude). If the address cannot be found, returns
    None.

    Address_to_Long_Lat("University of Oregon")
    >>> (44.0445359, -123.071734430929)

    Address_to_Long_Lat("made up address")
    >>> None
    '''

    #first, make sure address is sufficiently clear, and sanitize it
    address = address.lower()
    address = address.strip()

    if "eugene" not in address:
        address = address + " eugene"

    if "oregon" not in address:
        address = address + " oregon"

    #get coordinates from geolocator
    geolocator = Nominatim()
    location = geolocator.geocode(address)

    #check if geolocator accepted address. If not return None
    if location == None:
        return None

    #otherwise, get the longitude latitude coordinates
    lat = location[1][0]
    long = location[1][1]

    #return the coordinates in tuple format
    return (lat, long)


def Is_In_Bounds(address):
    '''
    (string) -> Boolean

    This function uses the Address_to_Long_lat() function described above,
    as well as the location information in BOUNDARIES to determine if an
    address falls within Safe Ride's boundaries or not. If the function recieves
    an address within Safe Ride's bounds, it will return True. In any other case
    it will return False

    Is_In_Bounds("University if Oregon")
    >>> True

    Is_In_Bounds("225 N 5th St, Springfield, OR 97477")
    >>> False

    Is_In_Bounds("")
    >>> False
    '''

    #get lat long
    coordinates = Address_to_Long_Lat(address)

    #make sure we got something, otherwise return False
    if coordinates == None:
        return False

    lat = coordinates[0]
    long = coordinates[1]

    #check if coordinates are west of first (western-most) region
    if long < BOUNDARIES[0][3]:
        return False

    #scan Eugene from west to east, checking if the coordinates fall within a
    #specified region
    for region in BOUNDARIES:
        if (long < region[2]) and (long >= region[3]) \
               and (lat < region[0]) and (lat > region[1]):
            return True

    return False


def Id_is_Valid(id):
    '''
    (int) -> Boolean

    This function checks if a student id is valid. It does this by verifying
    that it begins with '951' and is 9 characters long. If the id appears to
    be valid, the function returns True, otherwise False

    Id_is_Valid(951234567)
    >>> True

    Id_is_Valid(12345)
    >>> False

    Id_is_Valid(951123)
    >>> False
    '''

    #convert input to str
    id = str(id)

    if id[:3] != '951':
        return False

    if len(id) != 9:
        return False

    return True
