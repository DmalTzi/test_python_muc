import socket
import pickle

HOST = "0.0.0.0"
PORT = 5050
HEADINGSIZE = 10


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

def receive():
    full_msg = b''
    new_msg = True
    while True:
        msg = comm.recv(16)
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

def sended():
    msg = "Hello World, I'm from Server"
    msg = pickle.dumps(msg)
    msg = bytes(f"{len(msg):<{HEADINGSIZE}}", 'utf-8') + msg
    comm.send(msg)


while True:
    comm, addr = server.accept()
    print(f"Connected to {addr}")
    if True:
        receive()
        sended()