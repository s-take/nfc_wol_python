#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import socket
import os, sys

sys.path.insert(1, os.path.split(sys.path[0])[0])
from cli import CommandLineInterface

import nfc

f = open('addresslist.json', 'r')
data = json.load(f)
f.close()

def sendmagicpacket(macs, ipaddr, port):
  macstr = ''.join([x.decode('hex') for x in macs.split(':')])
  magicpacket = '\xff' * 6 + macstr * 16
  
  s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  s.sendto(magicpacket, ('10.11.135.255',port))
  print "OK"
  s.close()

def connected(tag):
  print tag

  if isinstance(tag, nfc.tag.tt3.Type3Tag):
    try:
      idm = str(tag.idm).encode("hex")
      mac = data[idm]['macaddr']
      ip = data[idm]['ipaddr']
      print mac
      print ip
      sendmagicpacket(mac,ip,9)
    except Exception as e:
      print "error: %s" % e
  else:
    print "error: tag isn't Type3Tag"

if __name__ == "__main__":
  clf = nfc.ContactlessFrontend('usb')
  clf.connect(rdwr={'on-connect': connected})
