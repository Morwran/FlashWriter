#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import sys, os

from terminal import Terminal
from write_image import WriteImage

port = "/dev/ttyUSB4"
baudrate=115200
stopbits=1
parity="N"
bytesizes=8

ADDR_HW="f1"

if __name__ =='__main__':

	if len (sys.argv) > 1:
		img_path=str(sys.argv[1])
		if(os.path.isfile(img_path)):
			print img_path
			#WriteImage(image_path=img_path,ADDR_HW=ADDR_HW)
			serObj = Terminal(
				port=port,baudrate=baudrate,
				stopbits=stopbits,parity=parity,
				bytesizes=bytesizes,
				ADDR_HW=ADDR_HW,
				image_path=img_path)
			serObj.close()
			serObj.open()
			serObj.clearFIFO()
			serObj.start()
		else:
			print "Error: Image path incorrect"	
	else:
		print "Error: Image path not set"	

