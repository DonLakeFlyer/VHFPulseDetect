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

	def __init__(self, drone, pulseQueue, channelIndex, pulseDetectBase):
		threading.Thread.__init__(self)

		print("UDPThread:init", pulseDetectBase)

		self.pulseQueue = pulseQueue
		self.channelIndex = channelIndex
		self.pulseDetectBase = pulseDetectBase
		self.sendIndex = 0

		if gpiozerioAvailable:
			self.cpuTemp = CPUTemperature()
		else:
			self.cpuTemp = None

		self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		if drone:
			# PDC Drone
			self.udpSocket.bind(('localhost', 10076))
			self.sendAddress = ('localhost', 10000) 
		else:
			# STE Tracker
			self.udpSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
			self.sendAddress = ('224.0.0.1', 5007) 
		self.udpSocket.setblocking(False)

	def run(self):
		while True:
			# Check for incoming commands
			try:
				data = self.udpSocket.recv(1024)
			except:
				pass
			else:
				self.parseCommand(data)

			pulseValue = self.pulseQueue.get(True)
			print("UDPThread pulseValue", pulseValue)

			temp = 0
			if self.cpuTemp:
				temp = self.cpuTemp.temperature

			packedData = struct.pack('<iiffii', 
							self.sendIndex,
							self.channelIndex, 
							pulseValue, 
							temp, 
							self.pulseDetectBase.get_pulse_freq(),
							self.pulseDetectBase.get_gain())
			try:
				self.udpSocket.sendto(packedData, self.sendAddress)
			except Exception as e:
				print("Exception UDPThread send", e)
			self.sendIndex = self.sendIndex + 1


	def parseCommand(self, commandBytes):
		command, value = struct.unpack_from('<ii', commandBytes)
		if command == 1:
			print("Gain changed ", value)
			self.pulseDetectBase.set_gain(value)
		elif command == 2: 
			print("Frequency changed ", value)
			self.pulseDetectBase.set_pulse_freq(value)
		else:
			print("Unknown command ", command, len(commandBytes))

#	def foo(self):
		# First see if we have a tcp connection
		#inputs = [ self.tcpSocketServer ]
		#outputs = []
		#readable, writable, exceptional = select.select(inputs, outputs, inputs, 0)
		#for s in readable:
		#    if s is server:
		#        print("TCP client accepting", client_address)
		#        self.tcpClient, client_address = s.accept()

		# Check for incoming commands
#		if self.tcpClient:
#			try:
#				data = self.tcpClient.recv(1024)
#			except:
#				pass
#			else:
#				self.parseCommand(data)
#
#		if math.isnan(pulseValue):
#			return
#
#		temp = 0
#		if self.cpuTemp:
#			temp = self.cpuTemp.temperature
#
#		packedData = struct.pack('<iiffii', 
#						self.sendIndex,
#						self.channelIndex, 
#						pulseValue, 
#						temp, 
#						self.pulseDetectBase.get_pulse_freq(),
#						self.pulseDetectBase.get_gain())
#		try:
#			self.udpSocket.sendto(packedData, self.sendAddress)
#			self.udpSocket.sendto(packedData, self.sendAddress)
#		except Exception as e:
#			print("Exception udp_sender:work Sending pulse to UDP socket", e)
#		if self.tcpClient:
#			try:
#				self.tcpClient.sendall(packedData)
#			except Exception as e:
#				print("Exception udp_sender:work Sending pulse to TCP socket", e)
#		self.sendIndex = self.sendIndex + 1

