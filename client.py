import socket
import pickle

HOST = "localhost"
PORT = 9090
HEADINGSIZE = 10


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))


# socket.send(b'Hello Sever')

while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = socket.recv(16)
        print(msg)
        print(type(msg))
        if new_msg:
            print(f"new message length: {msg[:HEADINGSIZE]}")
            msglen = int(msg[:HEADINGSIZE])
            print(type(msglen))
            new_msg = False
        
        full_msg += msg
        
        if len(full_msg) - HEADINGSIZE == msglen:
            print("Full msg recvd")
            print(full_msg[HEADINGSIZE:])
    
            d = pickle.loads(full_msg[HEADINGSIZE:])
            print(d)
    
            new_msg = True
            full_msg = b''