#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Enable one GPIO of the FTDI, wait DELAY seconds and disable all GPIOS """

import time
import sys
import ftdi1 as ftdi # libftdi-python and libftdi-1.3-2

VENDOR = 0x0403
PRODUCT = 0x6001
SERIAL = "A9KRJHHH"

BIT = 0x40
DELAY = 4

# For finding which bit to use:
#for i in range(8):
#    val = 2**i
#    print 'enabling bit #%d (0x%02x)' % (i, val)
#    ftdi.write_data(ftdic, chr(val), 1)
#    time.sleep (1)

def cycle_power(ftdic, description, serial):
    """ Power off for 4 seconds """

    ret = ftdi.usb_open_desc(ftdic, VENDOR, PRODUCT, description, serial)
    if ret < 0:
        print "Error opening USB device"
        sys.exit(1)

    ret = ftdi.set_bitmode(ftdic, BIT, ftdi.BITMODE_BITBANG)
    if ret < 0:
        print "Can't set bitbang mode"
        sys.exit(1)

    print "Cycling power"
    ftdi.write_data(ftdic, chr(BIT))
    time.sleep(DELAY)
    ftdi.write_data(ftdic, chr(0x00))

    time.sleep(0.3)
    ftdi.disable_bitbang(ftdic)

def main():
    """ Good old main"""

    ftdic = ftdi.new()
    if ftdic == 0:
        print "Failed to initialize"
        sys.exit(1)

    ret, devlist = ftdi.usb_find_all(ftdic, VENDOR, PRODUCT)
    if ret < 0:
        print "No FTDI devices found"
        sys.exit(1)

    curnode = devlist
    i = 0

    while curnode != None:
        ret, manufacturer, description, serial = ftdi.usb_get_strings(ftdic, curnode.dev)
        if ret < 0:
            print "Error getting information about FTDI devices"
            sys.exit(1)

        if serial == SERIAL:
            print 'Device #%d: %s %s (%s)\n' % (i, manufacturer, description, serial)
            cycle_power(ftdic, description, serial)

        curnode = curnode.next
        i += 1

    ftdi.usb_close(ftdic)
    ftdi.free(ftdic)

if __name__ == "__main__":
    main()

__author__ = "Peter Senna Tschudin"
__license__ = "GPLv2"
__version__ = "0.1"
