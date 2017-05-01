#!/usr/bin/python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import sys
import time
import argparse
import ConfigParser

import RPi.GPIO as GPIO
from pushbullet import Pushbullet

class robocoop:
    """Class for controlling a door"""

    def __init__(self, door_name, top_pin, bottom_pin, motor_a_pin, motor_b_pin, safety_limit, debug=False):
        self.name = door_name
        self.top_sensor_pin = top_pin
        self.bottom_sensor_pin = bottom_pin
        self.motor_a_pin = motor_a_pin
        self.motor_b_pin = motor_b_pin
        self.safety_limit = safety_limit
        self.debug = debug
        self.door_state = 'NULL'
        self.init_gpio()


    def init_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.top_sensor_pin, GPIO.IN)
        GPIO.setup(self.bottom_sensor_pin, GPIO.IN)
        GPIO.setup(self.motor_a_pin, GPIO.OUT)
        GPIO.setup(self.motor_b_pin, GPIO.OUT)


    def cleanup(self):
        GPIO.cleanup()


    def motor_off(self):
        GPIO.output(self.motor_a_pin, False)
        GPIO.output(self.motor_b_pin, False)


    def motor_up(self):
        GPIO.output(self.motor_a_pin, True)
        GPIO.output(self.motor_b_pin, False)


    def motor_down(self):
        GPIO.output(self.motor_a_pin, False)
        GPIO.output(self.motor_b_pin, True)


    def get_door_state(self):
        top_sensor = GPIO.input(self.top_sensor_pin)
        bottom_sensor = GPIO.input(self.bottom_sensor_pin)

        if top_sensor == 1 and bottom_sensor == 1:
            state = 'unknown'
        elif top_sensor == 0:
            state = 'opened'
        elif bottom_sensor == 0:
            state = 'closed'
        else:
            state = 'fubar'
        self.door_state = state


    def move_door(self, direction):
        self.get_door_state()
        if self.debug:
            print('Coop %s is %s, going to %s the coop.' % (self.name, self.door_state, direction))

        run_time = 0
        start_time = time.clock()
        if direction == 'open':
            while self.door_state != 'opened' and run_time < self.safety_limit:
                self.motor_up()
                self.get_door_state()
                run_time = time.clock() - start_time
        elif direction == 'close':
            while self.door_state != 'closed' and run_time < self.safety_limit:
                self.motor_down()
                self.get_door_state()
                run_time = time.clock() - start_time
        self.motor_off()

        return_msg = 'Coop %s is now %s |%.2fs|' % (self.name, self.door_state, run_time)
        return return_msg


def send_notification(api_key, message):
    pb = Pushbullet(api_key)
    my_channel = pb.channels[0]
    push = my_channel.push_note('RoboCoop', message)
    #pb.push_note('Chicken Door', message)


if __name__ == '__main__':
    description = ('ROBOCOOP - Open and close doors on a chicken coop via RPi.GPIO')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--direction', dest='direction',
                        choices=['open', 'close', 'auto'],
                        help='open, close, or auto')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='Print to Stdout and disable push notifications')
    parser.add_argument('--doors', dest='doors', nargs='*', default='NULL',
                        help='A space seperated list of door names to operate on')
    args, __ = parser.parse_known_args()

    config = ConfigParser.ConfigParser()
    config.read('robocoop.cfg')
    api_key = config.get('DEFAULT', 'pushbullet_api_key')
    if args.doors == 'NULL':
        doors = config.get('DEFAULT', 'doors_to_open').split(',')
    else:
        doors = args.doors

    status = 0
    for door in doors:
        try:
            try:
                obj = robocoop(door, config.getint(door, 'top_sensor_pin'),
                               config.getint(door, 'bottom_sensor_pin'),
                               config.getint(door, 'motor_a_pin'),
                               config.getint(door, 'motor_b_pin'),
                               config.getint(door, 'safety_limit'))
            except:
                print('No config found for door: %s' % door)

            if args.direction in ('open', 'close'):
                resp = obj.move_door(args.direction, args.debug)
            elif args.direction == 'auto':
                obj.get_door_state()
                if obj.door_state == 'unknown':
                    for x in range(1000):
                        obj.get_door_state()
                if obj.door_state == 'opened':
                    resp = obj.move_door('close', args.debug)
                elif obj.door_state == 'closed':
                    resp = obj.move_door('open', args.debug)
                else:
                    resp = "Did not move door. Door state is %s" % door_state
            else:
                obj.get_door_state()
                resp = 'The door is %s' % obj.door_state

            print(resp)
            if not args.debug:
                send_notification(api_key, resp)

        except:
            status = 69
            if not args.debug:
                send_notification(api_key, "Exception encountered")
            print("BOOM:", sys.exc_info())
        finally:
            obj.cleanup()

    sys.exit(status)
