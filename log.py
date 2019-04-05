#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Makenzie Brian
# File: log.py
# Description: Save data from Dymo M25 scale into csv file, file name should be participant number

# vendor_id=0x0922
# product_id=0x8003

"""
Handling raw data inputs example
"""

# FIX: auto shutoff,

import time
from msvcrt import kbhit
#from threading import Timer
import pywinusb.hid as hid
import math
#import schedule


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


# convert all data to grams or ounces (must be in correct mode)
def sample_handler(data):
    grams = data[4] + (256 * data[5])
    # ounces = 0.1 * (data[4] + (256 * data[5]))
    #print("Raw data: {0}    Grams: {1}".format(data, grams))

    global start
    #print(time.time() - start)
    if (round_up(time.time() - start, 1)) % 20 <= abs(.1):     # every 20 seconds, save data
        write_data(grams)
        print(grams)
        #print("to file")
        start = time.time()


# set device, open scale, pull data continuously
def raw_test():
    devices = hid.HidDeviceFilter(vendor_id=0x0922, product_id=0x8003).get_devices()
    scale = devices[0]

    #t = Timer(30.0, timeout)
    #t.start()

    if scale:
        while True:
            try:
                scale.open()
                scale.set_raw_data_handler(sample_handler)  # set custom raw data handler

                print("\nWaiting for data...\nPress any (system keyboard) key to stop...")
                while not kbhit() and scale.is_plugged():   # just keep the device opened to receive events
                    time.sleep(0.5)
                return

            finally:
                scale.close()

    else:
        print("There's not any non system HID class device available")


# write data to file
def write_data(datum):
    with open("000.csv", "a+") as csv_file:
        csv_file.write(str(datum))
        csv_file.write(",")
        #print(datum)


if __name__ == '__main__':
    #global start
    start = time.time()
    raw_test()
