import sys
import socket

def main():
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.bind(('localhost', 10000))
    sendAddress = ('localhost', 10001)
    while True:
        data, address = udpSocket.recvfrom(4*2)
        rgPulseInfo = struct.unpack('<if', data)
        sendIndex = rgPulseInfo[0]
        pulseValue = rgPulseInfo[1]
        print(pulseValue, sendIndex)

if __name__ == '__main__':
    main()
