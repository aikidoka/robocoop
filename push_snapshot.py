#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from pushbullet import Pushbullet
import sys
import time
import ConfigParser
import subprocess


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('chicken_door.cfg')
    api_key = config.get('pushbullet', 'api_key')
    pb = Pushbullet(api_key)

    try:
        cmd = "v4l2grab -d /dev/video0 -o /tmp/coop_door.jpg"
        subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        with open("/tmp/coop_door.jpg", "rb") as pic:
            file_data = pb.upload_file(pic, "coop_door.jpg")
        push = pb.push_file(**file_data)

    except:
        print "BOOM:", sys.exc_info()
