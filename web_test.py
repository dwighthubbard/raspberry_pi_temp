#!/usr/bin/python
from __future__ import print_function
import os
import glob
import random
from redis_collections import List as RedisList
import redislite
import sys
import time


# Redis RDB backing filename
# By specifying a redisrdb file to redislite we ensure
# the data persists after the program exits.
redisrdb = '/tmp/temp.rdb'

# How frequently in seconds we want to get the temp readings
frequency = 1

last_reading = 0.0

class DeviceReadError(Exception):
    """
    Exception class for errors reading a device.  This allows
    our program to be able to trap errors reading data from the
    sensor.
    """
    pass


# Functions to read the temp sensor
def read_temp_c():
    """
    Read the temp in Celsius

    Returns
    -------
    temp: float
        The temp from the sensor in Celsius.

    Raises
    ------
    DeviceReadError
        Unable to read values from the temp sesnsor.
    """
    global last_reading
    last_reading = random.uniform(0, 100)
    return last_reading


def read_temp_f():
    """
    Read the temp in Fahrenheit

    Returns
    -------
    temp: float
        The temp from the sensor in Fahrenheit.
    """
    return last_reading * 9.0 / 5.0 + 32.0


if __name__ == '__main__':
    # Redis is key/value store.  It provides a way to store data 
    # structures to a service that is seperate from the running 
    # program.  Many of the data structures Redis can store are
    # nearly identical to standard Python built in data types such
    # as lists and dictionaries.  
    # We are using the RedisList object from the redis_collections 
    # module to access Redis.  This provides us with a python 
    # object that works almost exactly like a normal Python list, 
    # except the information is stored in Redis.
    # This means the information in the list can persist between
    # program runs or be stored to mulitple Redis servers using
    # Redis repliataion.
    # Unlike SQL databases, the default Redis configuration will
    # do a single disk write operation every 15 minutes instead
    # every time data is written.  This significantly decreases
    # wear on flash/sd-card.
    # We are going to create two lists in Redis to store our temps
    # one for celsius and one for fahranheit.
    redis_connection = redislite.StrictRedis(redisrdb)
    temp_c_list = RedisList(redis=redis_connection, key='temp_c')
    temp_f_list = RedisList(redis=redis_connection, key='temp_f')

    del temp_c_list[:]
    del temp_f_list[:]
    
    # Now loop through 
    while True:
        temp_c_list.append(read_temp_c())
        temp_f_list.append(read_temp_f())
        print('Temp F:', read_temp_f(), 'Hourly Average Temp F:', sum(temp_f_list[-3600:])/len(temp_f_list[-3600:]))
        time.sleep(frequency)
