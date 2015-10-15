#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import RPi.GPIO as GPIO
from pushbullet import Pushbullet
import sys
import time
import argparse
import ConfigParser


def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(config.getint('gpio', 'top_sensor_pin'), GPIO.IN)
    GPIO.setup(config.getint('gpio', 'bottom_sensor_pin'), GPIO.IN)
    GPIO.setup(config.getint('gpio', 'motor_a_pin'), GPIO.OUT)
    GPIO.setup(config.getint('gpio', 'motor_b_pin'), GPIO.OUT)


def motor_off():
    GPIO.output(config.getint('gpio', 'motor_a_pin'), False)
    GPIO.output(config.getint('gpio', 'motor_b_pin'), False)


def motor_up():
    GPIO.output(config.getint('gpio', 'motor_a_pin'), True)
    GPIO.output(config.getint('gpio', 'motor_b_pin'), False)


def motor_down():
    GPIO.output(config.getint('gpio', 'motor_a_pin'), False)
    GPIO.output(config.getint('gpio', 'motor_b_pin'), True)


def get_door_state():
    top_sensor = GPIO.input(config.getint('gpio', 'top_sensor_pin'))
    bottom_sensor = GPIO.input(config.getint('gpio', 'bottom_sensor_pin'))

    if top_sensor == 1 and bottom_sensor == 1:
        state = 'unknown'
    elif top_sensor == 0:
        state = 'opened'
    elif bottom_sensor == 0:
        state = 'closed'
    else:
        state = 'fubar'
    return state


def move_door(direction):
    safety_limit = config.getint('chickendoor', 'safety_limit')
    door_state = get_door_state()
    print 'door state is %s, going to %s door' % (door_state, direction)
    run_time = 0
    start_time = time.clock()
    if direction == 'open':
        while door_state != 'opened' and run_time < safety_limit:
            motor_up()
            door_state = get_door_state()
            run_time = time.clock() - start_time
    elif direction == 'close':
        while door_state != 'closed' and run_time < safety_limit:
            motor_down()
            door_state = get_door_state()
            run_time = time.clock() - start_time
    motor_off()
    return_msg = 'The door is now %s |%ss|' % (door_state, run_time)
    print return_msg
    return return_msg


def send_notification(api_key, message):
    pb = Pushbullet(api_key)
    pb.push_note('Chicken Door', message)


if __name__ == '__main__':
    description = ('Script to open and close a rpi chicken door')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--direction', dest='direction',
                        choices=['open', 'close', 'auto'],
                        help='open, close, or auto')
    parser.add_argument('--silent', dest='silent', action='store_true',
                        help='Will disable the sending of notifications')
    args, __ = parser.parse_known_args()

    config = ConfigParser.ConfigParser()
    config.read('gpio.cfg')
    api_key = config.get('pushbullet', 'api_key')

    status = 0
    try:
        init_gpio()
        if args.direction in ('open', 'close'):
            resp = move_door(args.direction)
        elif args.direction == 'auto':
            door_state = get_door_state()
            if door_state == 'opened':
                resp = move_door('close')
            elif door_state == 'closed':
                resp = move_door('open')
            else:
                resp = "Did not move door. Door state is %s" % door_state
        else:
            door_state = get_door_state()
            print 'door is %s |%ss|' % door_state

        if not args.silent:
            send_notification(api_key, resp)

    except:
        status = 69
        if not args.silent:
            send_notification(api_key, "Exception encountered")
        print "BOOM:", sys.exc_info()

    GPIO.cleanup()
    sys.exit(status)
