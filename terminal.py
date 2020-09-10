#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import numpy as np

from collections import deque, namedtuple 

from threading import Thread

from rpi_serial import RpiSerial

from write_image import WriteImage

import sys, time



class Terminal(RpiSerial,WriteImage):
	def __init__(self,port,baudrate,stopbits,parity,bytesizes,ADDR_HW,image_path):
		RpiSerial.__init__(self,port,baudrate,stopbits,parity,bytesizes)
		WriteImage.__init__(self,image_path,ADDR_HW)

		self.ADDR_HW = ADDR_HW

		self.WREN = True

		self.type_cmd = ''

		self.msg_dict={
			'boot':
				{
					'err:':['',False],
					'wrn:':['',False],
					'msg:':['',False]
				},
			'rply':''
			}


		#self.list_args =[]


	def terminal(self):
		return raw_input("command: ")		

	def start(self):
		self.t1 = Thread(target=self.th_read, args=())
		self.t2 = Thread(target=self.th_write, args=())
		self.t1.start()
		self.t2.start()
		self.t1.join()
		self.t2.join()


	def collect(self):
		self.read_str = self.read()	
		
		if(self.read_str):
			if(len(self.read_str.split())>1):
				print self.read_str
				if self.read_str.split()[0] in self.msg_dict:  #проверяем наличие идентификатора в словаре
					#print self.d.keys()[1:]
					self.type_cmd = self.read_str.split()[0] #идентификатор сообщения
	
					
					if self.type_cmd=='boot':
						type_boot_msg = self.read_str.split()[1]
						if type_boot_msg in self.msg_dict[self.type_cmd]:
							boot_msg = self.read_str.split()[2]
							if(len(boot_msg)>0):
								
	
								if(type_boot_msg=='err:' or type_boot_msg=='wrn:'):
									
									
									if(not self.msg_dict[self.type_cmd][type_boot_msg][1]):
										
										self.msg_dict[self.type_cmd][type_boot_msg][1] = True
										self.msg_dict[self.type_cmd]['msg:'][1] = False
										self.msg_dict[self.type_cmd][type_boot_msg][0] = boot_msg
										print type_boot_msg + ' ' + boot_msg
										return 0
								if type_boot_msg=='msg:':
	
									
									if(not self.msg_dict[self.type_cmd][type_boot_msg][1]):
										
										self.msg_dict[self.type_cmd][type_boot_msg][1] = True
										self.msg_dict[self.type_cmd]['err:'][1] = False
										self.msg_dict[self.type_cmd]['wrn:'][1] = False
										self.msg_dict[self.type_cmd][type_boot_msg][0] = boot_msg
										print type_boot_msg + ' ' + boot_msg
										return 0 
					#else:
					#	print self.read_str			



	
	def th_read(self):
		while 1:
			self.collect()
			

	
	def th_write(self):
		eol='\r\n'
		while 1:
			#print "2"
			#time.sleep(0.5)
			self.cmd=self.terminal()
			if len(self.cmd)==1:
				if ord(self.cmd)==27:
					print"Exiting..."
					sys.exit()
					self.close()
					
					break
			elif len(self.cmd)>1:
				if self.cmd=='write':
					
					if not self.msg_dict['boot']['err:'][1]:
						crc, size = self.param_im()
						#if self.msg_dict['boot']['msg:'][1] or self.msg_dict['boot']['wrn:'][1]:
						#	msg1="uart stop {}".format(self.ADDR_HW)
						#	print msg1 
						#	self.write_byte(msg1)
						#	time.sleep(0.1)
						
						#msg1="uart stop {}".format(self.ADDR_HW)
						#print msg1 
						#self.write_byte(msg1)
						#time.sleep(0.1)

						msg2="boot srec {} {} {} {}".format(size,crc,int(self.WREN),self.ADDR_HW)
						print msg2
						self.write_byte(msg2)
						time.sleep(5)

						#msg_wren = "fl wren {}".format(self.ADDR_HW)
						#print msg_wren
						#self.write_byte(msg_wren)
						#time.sleep(1)

						print"Loading image..."
						if -1==self.write_im():
							print"err image write"
							msg_brk = "boot brk {}".format(ADDR_HW)
							print msg_brk 
							self.write_byte(msg_brk)
					else:
						print"device not ready"
		





				elif self.cmd=='test':	
					self.param_im()	

				else:
					
					self.write_byte(self.cmd)
					











