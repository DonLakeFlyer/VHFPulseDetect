import threading
import math
import subprocess
import socket
import select
import struct
import time

try:
    from gpiozero import CPUTemperature
except:
    gpiozerioAvailable = False
else:
    gpiozerioAvailable = True

class UDPThread (threading.Thread):
	exitFlag = False

	def __init__(self, pulseQueue):
		threading.Thread.__init__(self)

		self.pulseQueue = pulseQueue
		self.sendIndex = 0
		self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.udpSocket.bind(('localhost', 10076))
		self.sendAddress = ('localhost', 10000) 
		self.udpSocket.setblocking(False)

	def run(self):
		while True:
			pulseValue = self.pulseQueue.get(True)
			print("UDPThread pulseValue", pulseValue)

			packedData = struct.pack('<if', self.sendIndex, pulseValue)
			try:
				self.udpSocket.sendto(packedData, self.sendAddress)
			except Exception as e:
				print("Exception UDPThread send", e)
			self.sendIndex = self.sendIndex + 1
