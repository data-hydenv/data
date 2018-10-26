#!/bin/python3
"""Dirty script for reading a PM sensor

Stream PM25 and PM10 readings from a nova SDS011 into a csv file.
This script is only tested on Linux and is made for python 3.
"""
import serial, struct, time
from datetime import datetime as dt


def read(s):
    # we need the current and last byte to find the message start
    byte, lastbyte = b'\x00', b'\x00'

    # loop until message is found
    while True:
        lastbyte = byte
        byte = s.read(1)

        # start byte found?
        if lastbyte == b'\xAA' and byte == b'\xC0':
            # read the whole block
            block = s.read(8)

            # decode
            # little endian low byte to high byte
            msg = struct.unpack('<hhxxcc', block)

            # get the values
            pm25 = msg[0] / 10.
            pm10 = msg[1] / 10.

            return pm10, pm25


def start(dev, baud=9600, fname='pm.csv', step_sec=15, to_file=True):
    try:
        s = serial.Serial(dev, baud)
    except serial.SerialException:
        raise ValueError('Device %s not found.' % dev)

    while True:
        # get the reading
        pm10, pm25 = read(s)

        # save to file
        if to_file:
            with open(fname, 'a') as csv:
                t = '%s,%.1f,%.1f\n' % (
                    dt.strftime(dt.utcnow(), '%Y-%m-%d %H:%M:%S'),
                    pm10, pm25
                )
                csv.write(t)

        # and print
        print('PM10: {} ug/cm3\t\tPM25: {}ug/cm3'.format(pm10, pm25))

        # sleep
        time.sleep(step_sec)

if __name__=='__main__':
    import sys
    if len(sys.argv) <= 1:
        raise ValueError('At least the device USB port has to be specified')
    start(*sys.argv[1:])