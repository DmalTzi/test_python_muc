import socket
import pickle

HOST = "localhost"
PORT = 5050
HEADINGSIZE = 10


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

def receive():
    full_msg = b''
    new_msg = True
    while True:
        msg = socket.recv(16)
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
            break

def send():
    msg = "Hello World, I'm from Client"
    msg = pickle.dumps(msg)
    msg = bytes(f"{len(msg):<{HEADINGSIZE}}", 'utf-8') + msg
    socket.send(msg)


while True:
    if True:
        send()
        receive()
        break