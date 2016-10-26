"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments. 
#

BREVET_TABLE = [ [0, 200, 15, 34], [200, 400, 15, 32], [400, 600, 15, 30], [600, 1000, 11.428, 28] ]
# BREVET_TABLE models the brevet controle table at https://rusa.org/octime_alg.html with entries in the form of 
# [section start, section end, minimum speed, maximum speed] measured in km and km/hr
BREVET_LENGTHS = [200, 300, 400, 600, 1000] # legal brevet lengths in km

def calc_open( controle_dist, brevet_dist ):
    """
    Args:
        controle_dist: number, the location of the controle (measured in km from the starting line)
        brevet_dist: number, total length of the brevet, must be 200, 300, 400, 600 or 1000 exactly
        (these are the only official acp brevet lengths)
    Returns:
        The number of hours a rider has before a controle at controle_dist km
        opens on a brevet_dist km length brevet 
    """
    hrs = 0
    for el in BREVET_TABLE:
        if el[1] < controle_dist: #the controle is after the end of the current section
            hrs += (el[1] - el[0]) / el[3] #add the time allowed to go from the section start to its end
        elif (el[1] > controle_dist) & (controle_dist > el[0]): #the control is in the current section
            hrs += (controle_dist - el[0]) / el[3] #add time allowed to go from the section start to the controle
        else: # if neither statement triggers the controle is before this section starts and there is no time to add
            hrs += 0 # present for clarity, nothing to do in this case
    return hrs


def calc_close( controle_dist, brevet_dist ):
    """
    Args:
        controle_dist: number, the location of the controle (measured in km from the starting line)
        brevet_dist: number, total length of the brevet, must be 200, 300, 400, 600 or 1000 exactly
        (these are the only official acp brevet lengths)
    Returns:
        The number of hours a rider has before a controle at controle_dist km
        closes on a brevet_dist km length brevet 
    """
    hrs = 0
    for el in BREVET_TABLE:
        if el[1] < controle_dist: #the controle is after the end of the current section
            hrs += (el[1] - el[0]) / el[2] #add the time allowed to go from the section start to its end
        elif (el[1] > controle_dist) & (controle_dist > el[0]): #the control is in the current section
            hrs += (controle_dist - el[0]) / el[2] #add time allowed to go from the section start to the controle
        else: # if neither statement triggers the controle is before this section starts and there is no time to add
            hrs += 0 # present for clarity, nothing to do in this case
    if controle_dist == 200 & brevet_dist == 200:
        hrs = 13.5 # according to acp stardards a 200km control on a 200km brevet is 13H30 which equals 13.5H
    if controle_dist == 0:
        hrs = 1 # riders have 1 hour to leave the starting line 
    return hrs


def add_hours( hrs, start_time ):
    """
    Args:
        hrs: number, hours to add to start_time, decimals accepted
        start_time: an arrow object, time hrs must be added to
    Returns:
        an arrow object, the time it will be hrs hours after start_time
    """
    return_time = start_time
    num_minutes = (hrs % 1) * 60 #convert decimal portion of hrs to minutes
    num_hours = hrs // 1 # floor hrs to get a whole number
    return_time = return_time.replace(hours=+num_hours) # add num_hours to return_time
    return_time = return_time.replace(minutes=+num_minutes) # add num_minutes to return_time
    return return_time


def open_time( control_dist_km, brevet_dist_km, brevet_start_time ):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet in kilometers,
           which must be one of 200, 300, 400, 600, or 1000 (the only official
           ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    arrow_brevet_start = arrow.get(brevet_start_time) # store start time in an arrow object for easy reference
    error_time = arrow_brevet_start.replace(hours = -25) #subtract one from day and hour of start time to denote error
    #sanitize input
    if not brevet_dist_km in BREVET_LENGTHS: # brevet_dist_km is not an acp brevet length
        print("illegal brevet length {}".format(brevet_dist_km))
        return error_time.isoformat() # return start of epoch to denote error
    if control_dist_km > brevet_dist_km & control_dist_km < 1.2 * brevet_dist_km:
        # controles 20% past the brevet distance are allowed
        control_dist_km = brevet_dist_km # the controles are timed as though they were at the brevet length
    if control_dist_km > 1.2 * brevet_dist_km: # controls exceeding 120% of the brevet length aren't allowed
        print("controle distance exceeds 120% of brevet distance")
        return error_time.isoformat() # return start of epoch to denote error

    #calculate return value
    hrs = calc_open(control_dist_km, brevet_dist_km) # get hrs from brevet start till the controle opens
    ret_time = add_hours(hrs, arrow_brevet_start) # add hrs to brevet start time
    return ret_time.isoformat() # return in iso format


def close_time( control_dist_km, brevet_dist_km, brevet_start_time ):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet in kilometers,
           which must be one of 200, 300, 400, 600, or 1000 (the only official
           ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    #sanitize input
    if not (brevet_dist_km in BREVET_LENGTHS): # brevet_dist_km is not an acp brevet length
        print("illegal brevet length")
        return arrow.get(0).isoformat() # return start of epoch to denote error
    if control_dist_km > brevet_dist_km & control_dist_km < 1.2 * brevet_dist_km:
        # controles 20% past the brevet distance are allowed
        control_dist_km = brevet_dist_km # the controles are timed as though they were at the brevet length
    if control_dist_km > 1.2 * brevet_dist_km: # controls exceeding 120% of the brevet length aren't allowed
        print("controle distance exceeds 120% of brevet distance")
        return arrow.get(0).isoformat() # return start of epoch to denote error


    hrs = calc_close(control_dist_km, brevet_dist_km) # get the hours to elapse between brevet start and controle close 
    ret_time = add_hours(hrs, arrow.get(brevet_start_time)) # add hrs hours to brevet start time
    return ret_time.isoformat() #return in iso format

