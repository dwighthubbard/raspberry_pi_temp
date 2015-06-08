#!/usr/bin/python
from __future__ import print_function
import os
import glob
import time
import redislite
from redis_collections import List as RedisList


# Redis RDB backing filename
redisrdb = '/tmp/temp.rdb'


class DeviceReadError(Exception):
    pass


# Functions to read the temp sensor
def read_temp_c():
    """
    Read the temp in C

    Returns
    -------
    temp; float
        The temp from the sensor in Celsius.

    Raises
    ------
    DeviceReadError
        Unable to read values from the temp sesnsor.
    """
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    value = -1
    with open(device_file) as file_handle:
        lines = [line.strip().split()[-1] for line in file_handle.readlines()]
    if lines[0] == "YES":
        if lines[1].startswith('t='):
            value = lines[1][2:]
    if value == -1:
        raise DeviceReadError('Unable to access temp sensor')
    return float(value)/1000.0


def read_temp_f():
    """
    Read the temp in F

    Returns
    -------
    temp; float
        The temp from the sensor in Farenheit.

    Raises
    ------
    DeviceReadError
        Unable to read values from the temp sesnsor.
    """
    return read_temp_c() * 9.0 / 5.0 + 32.0


if __name__ == '__main__':
    # Make sure the kernel modules to read the temp sensor are loaded
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    # Create two list in Redis to store our temps
    redis_connection = redislite.StrictRedis(redisrdb)
    temp_c_list = RedisList(redis=redis_connection, key='temp_c')
    temp_f_list = RedisList(redis=redis_connection, key='temp_f')

    while True:
        temp_c_list.append(read_temp_c())
        temp_f_list.append(read_temp_f())
        print('Temp F:', read_temp_f(), 'Hourly Average Temp F:', sum(temp_f_list[-3600:])/len(temp_f_list[-3600:]))
        time.sleep(1)
