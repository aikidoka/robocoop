     ____            __              ____
    /\  _`\         /\ \            /\  _`\
    \ \ \L\ \    ___\ \ \____    ___\ \ \/\_\    ___     ___   _____
     \ \ ,  /   / __`\ \ '__`\  / __`\ \ \/_/_  / __`\  / __`\/\ '__`\
      \ \ \\ \ /\ \L\ \ \ \L\ \/\ \L\ \ \ \L\ \/\ \L\ \/\ \L\ \ \ \L\ \
       \ \_\ \_\ \____/\ \_,__/\ \____/\ \____/\ \____/\ \____/\ \ ,__/
        \/_/\/ /\/___/  \/___/  \/___/  \/___/  \/___/  \/___/  \ \ \/
                                                                 \ \_\
                                                                  \/_/
RoboCoop
========
Collection of scripts to operate a chicken door system. Based on the wiring design in https://github.com/ericescobar/Chicken_Door


Setup
-----
Clone and create robocoop.cfg. Or an Ansible role is now included, see README in ./ansible. 


Notable Files
-------------
- robocoop.py - interface to open and close the door
- robocoop.cfg - required config for gpio settings
- poller.py - returns a json dictionary of the door sensor's data
- ansible/ - an ansible role to provision an ArchARM RPI
