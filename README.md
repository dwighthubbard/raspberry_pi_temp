raspberry_pi_temp
=================

This is an example of logging a temp data from a one wire temp sensor
to a Redis server using the redislite and redis-collections modules.

This provides a couple of advantages over logging the data using a
sql database;

1. It's easier to use.
   Redis supports storing lists and dictionaries.  Which means it does
   not require setting up and managing a database schema.  Modules like
   the redis-collections module provide Redis List objects that provide
   Python like List objects that store their data in Redis. 
   
2. It doesn't wear out your flash/sd-card
   Redis by default does not write the data to flash every time new
   information is added.  It will by default write once ever 15 minutes
   or when it is shutdown.  This results in a lot less wear on the
   sd-card.

**The redislite module will install, configure and manage the redis
server.  So there is no need to deal with setting up a seperate redis
server**

The steps to use this script are:

1. Wire up the temp sensor to your raspberry pi (see https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview
for a good tutorial on how to do this)

2. Install the redislite and redis-collections python modules using the
   python pip packgae manager.

  $ pip install redislite redis-collctions
  
3. Run the script as root

  $ sudo python raspberry_pi_temp.py
  
