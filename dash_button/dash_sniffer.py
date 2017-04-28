#!/bin/python2
#
# Quick little script to listen for ARP requests for network GW from Dash Buttons

from scapy.all import *
from subprocess import call

def arp_display(pkt):
    if pkt[ARP].op == 1:
        if pkt[ARP].hwsrc == '44:65:0d:9c:29:e0' and pkt[ARP].pdst == '192.168.42.1':
            print 'dash button (%s)' % pkt[ARP].hwsrc
            call('/opt/robocoop/opendoor.sh')
	elif pkt[ARP].hwsrc == '44:dd:0d:9c:29:e0' and pkt[ARP].pdst == '192.168.42.1':
            print 'dash button (%s)' % pkt[ARP].hwsrc
            call('/opt/robocoop/closedoor.sh')

while True:
   sniff(prn=arp_display, filter='arp', store=0, count=10) 
