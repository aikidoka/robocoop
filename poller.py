#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import RPi.GPIO as GPIO
import sys
import ConfigParser


def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(config.getint('gpio', 'top_sensor_pin'), GPIO.IN)
    GPIO.setup(config.getint('gpio', 'bottom_sensor_pin'), GPIO.IN)


def get_sensor_state():
    top_sensor = GPIO.input(config.getint('gpio', 'top_sensor_pin'))
    bottom_sensor = GPIO.input(config.getint('gpio', 'bottom_sensor_pin'))

    sensors = {'top': top_sensor, 'bottom': bottom_sensor}
    return sensors


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('chicken_door.cfg')

    try:
        init_gpio()
        print get_sensor_state()

        #TODO: PUBLISH TO SOMETHING

    except:
        print "BOOM:", sys.exc_info()

    GPIO.cleanup()
    sys.exit()
