#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import sys, os

from terminal import Terminal
from write_image import WriteImage

port = "/dev/ttyUSB0"
baudrate=115200
stopbits=1
parity="N"
bytesizes=8

#ADDR_HW="f0"

if __name__ =='__main__':

	if len (sys.argv) == 2:
		img_path=str(sys.argv[1])
		if(os.path.isfile(img_path)):
			print img_path
			#WriteImage(image_path=img_path,ADDR_HW=ADDR_HW)
			addr_hw=str(sys.argv[2])
			print addr_hw
			serObj = Terminal(
				port=port,baudrate=baudrate,
				stopbits=stopbits,parity=parity,
				bytesizes=bytesizes,
				ADDR_HW=addr_hw,
				image_path=img_path)
			serObj.close()
			serObj.open()
			serObj.clearFIFO()
			serObj.start()
		else:
			print "Error: Image path incorrect"	
	else:
		print "Error: Image path not set"	

