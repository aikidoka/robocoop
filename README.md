rpi-chicken-door
--------
Collection of scripts to operate a chicken door system. Based on the wiring design in https://github.com/ericescobar/Chicken_Door


Setup
--------
Be sure to create the chicken_door.cfg file. A sample is included in the repo as chicken_door.cfg.sample. Example systemd service and timers included.


Files
--------
- Door_Control.py - interface to open and close the door
- poller.py - returns a dictionary of the sensor's data
- push_snapshot.py - sends a pushbullet image of the door state
    - requires v4l2grab (https://github.com/twam/v4l2grab.git)
