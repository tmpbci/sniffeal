#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Sniff packets from interface en0 using python module scapy (2.3.1)
and generate led color for bhoreal in usb midi mode depending on packet port number

Led are midi notes (0 to 63)
Color is a midi parameter (velocity) so 0 to 127.

To modify the network interface (wifi/ethernet), change it in the last code line.

Uses mido to send MIDI messages directly in python.

v0.3
By Sam Neurohack
LICENCE : CC 
'''
 
import mido
from mido import Message
from time import sleep
import types
import random
from scapy.all import *

outport = mido.open_output('Arduino Leonardo')

counter = 0

def sendled(zzzport):
	global counter
	
	zzz = zzzport % 127												# zzz = led color
	msgout = mido.Message('note_on', note=counter, velocity=zzz)
					
	outport.send(msgout)
	sleep(0.001)
	counter += 1
	if counter > 63:
		counter = 0


def print_summary(pkt):
    if IP in pkt:
        ip_src=pkt[IP].src
        ip_dst=pkt[IP].dst
        
        
    	if TCP in pkt:
        	tcp_sport=pkt[TCP].sport
        	tcp_dport=pkt[TCP].dport

        	if tcp_sport < 50000:
        		print " IP src " + str(ip_src) + " TCP sport " + str(tcp_sport) 
        		sendled(tcp_sport)
        	if tcp_dport < 50000:
        		print " IP dst " + str(ip_dst) + " TCP dport " + str(tcp_dport)
        		sendled(tcp_dport)
        if UDP in pkt:
        	udp_sport=pkt[UDP].sport
        	udp_dport=pkt[UDP].dport

        	if udp_sport < 50000:
        		print " IP src " + str(ip_src) + " UDP sport " + str(udp_sport) 
        		sendled(udp_sport)
        	
        	if udp_dport < 50000:
        		print " IP dst " + str(ip_dst) + " UDP dport " + str(udp_dport)
        		sendled(udp_dport)


	if ARP in pkt and pkt[ARP].op in (1,2):
		print " ARP"
		sendled(67)
        	


def handle_error(self,request,client_address):		# All callbacks
    pass

sniff(iface='en0', prn=print_summary, store=0)
