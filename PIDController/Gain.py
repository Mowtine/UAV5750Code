import threading
import time
import socket

class ReadGain:
    def __init__(self,ip,port):
        self.TCP_IP = ip  #change here
        self.TCP_PORT = port
        self.BUFFER_SIZE = 1024
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.TCP_IP, self.TCP_PORT))

    def ReaderThread(self):
        while(1):
            self.gain = self.s.recv(self.BUFFER_SIZE)
            self.gain = pickle.loads(self.gain)

    def GetValues(self):
        return self.gain

    def run(self, name):
        thread = threading.Thread(target = self.get_values)
        thread.start()
