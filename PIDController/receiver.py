import socket
import pickle
import time

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

start_time = time.time()
while(1):
    data = s.recv(BUFFER_SIZE)
    data = pickle.loads(data)
    print(data)
