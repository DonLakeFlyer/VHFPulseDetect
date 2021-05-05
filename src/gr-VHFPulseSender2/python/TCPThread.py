import threading
import math
import subprocess
import socket
import select
import struct

try:
    from gpiozero import CPUTemperature
except:
    gpiozerioAvailable = False
else:
    gpiozerioAvailable = True

class TCPThread (threading.Thread):
	exitFlag = False

	def __init__(self, pulseQueue, channelIndex, pulseDetectBase):
		threading.Thread.__init__(self)

		self.pulseQueue = pulseQueue
		self.channelIndex = channelIndex
		self.pulseDetectBase = pulseDetectBase
		self.sendIndex = 0

		if gpiozerioAvailable:
			self.cpuTemp = CPUTemperature()
		else:
			self.cpuTemp = None

		self.tcpSocketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcpAddress = ('', 50000)
		self.tcpSocketServer.bind(self.tcpAddress)
		self.tcpSocketServer.listen(1)
		self.tcpClient = None

	def run(self):
		while True:
			print("Waiting on TCP client connection")
			self.tcpClient, clientAddress = self.tcpSocketServer.accept()
			self.tcpClient.setblocking(False)
			print("TCP connected", clientAddress)

			while True:
				# Check for incoming commands
				try:
					data = self.tcpClient.recv(8)
				except:
					pass
				else:
					if len(data) == 8:
						self.parseCommand(data)

				pulseValue = self.pulseQueue.get(True)
				print("TCPThread pulseValue", pulseValue)

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
					self.tcpClient.sendall(packedData)
				except Exception as e:
					client = self.tcpClient
					self.tcpClient = None
					print("Exception TCPThread send", e)
					try:
						client.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
					except:
						pass
					try:
						client.close()
					except:
						pass
					print("TCP connection closed")
					break
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
