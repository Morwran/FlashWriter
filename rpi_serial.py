#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import serial, time
#from PyQt4 import QtGui
#from PyQt4.QtGui import QWidget

class RpiSerial():
	def __init__(self,port,baudrate,stopbits,parity,bytesizes):
		self.port=port
		self.baudrate=int(baudrate)
		self.stopbits=int(stopbits)
		self.bytesizes=int(bytesizes)
		self.parity=parity

		try:
			self.ser=serial.Serial(port=self.port,baudrate=self.baudrate,stopbits=self.stopbits,\
				bytesize=self.bytesizes,parity=self.parity,timeout=0.1, xonxoff=False, rtscts=False,\
				writeTimeout=0, dsrdtr=False, interCharTimeout=None)
		except serial.SerialException:
			#QtGui.QMessageBox.warning(QWidget(), "Warning", u"вставь COM-PORT")
			print "вставь COM-PORT"
			#return -1


	def open(self):
		try:
			self.ser.open()
			
		except serial.SerialException:
			print "cant open port"
			return -1

	def write(self,data):
		self.ser.flushInput()
		try:
			self.ser.write(str(data))
		except serial.SerialException:
			print "cant write data"
			return -1

		return 0	
	def write_byte(self,data):
		self.ser.flushInput()
		for i in data:
			self.write(i)
			time.sleep(0.001) #0.2
			self.ser.flushInput()
		#self.write('\r')
		self.write('\n')
		#self.clearFIFO()		

	def read(self):
		try:
			#readdata = self.ser.readlines()
			readdata = self.ser.read_until(terminator='\r\n',size=None)
		except serial.SerialException as e:
			print "cant read data"
			print e
			return
		if readdata==[]: print "error read data"
		
		return readdata

	def close(self):
		try: self.ser.close()
		except Exception: pass

	def clearFIFO(self):
		try:
			self.ser.flushInput()
			self.ser.flushOutput()
		except serial.SerialException: pass	