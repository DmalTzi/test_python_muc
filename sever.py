import socket
import pickle



HOST = "localhost"
PORT = 9090
HEADINGSIZE = 10
sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sever.bind((HOST, PORT))

sever.listen()

while True:
    comm, addr = sever.accept()
    print(f"Connected to {addr}")

    msg = "Welcome to the sever!"
    # d = {1:"Hey",2:"There"}
    msg = pickle.dumps(msg)

    msg = bytes(f"{len(msg):<{HEADINGSIZE}}", 'utf-8') + msg

    # data = comm.recv(1024)
    # print(data)
    # if data:
    #     print("MSG From Client")

    comm.send(msg)
