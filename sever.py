import socket
import json
from pymongo import MongoClient

HOST = '0.0.0.0'
PORT = 9090
MONGO_URL = "mongodb+srv://hdrproject:50230@cluster0.ktm1unb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
db = client.HDRProjecct
collection = db.wtfs


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Waiting for connection...")
client_socket, client_address = server_socket.accept()
print("Connected to:", client_address)

box = {}

while True:
    data = client_socket.recv(1024)
    if data.decode('utf-8') == '0':
        break 
    findone = collection.find_one({"Detail.Serial":int(data)})
    print(findone)
    if findone:
        symptom = findone["Symptom"]
        send_status = findone["Detail"]["SendStatus"]
        send_by = findone["Detail"]["SendBy"]
        if symptom:
            if symptom == "มีไข้" or symptom == "ปวดหัว":
                box["type"] = 0
            elif symptom == "ปวดประจำเดือน":
                box["type"] = 1
            elif symptom == "ท้องเสีย":
                box["type"] = 2
            elif symptom == "ลมพิษ/แพ้":
                box["type"] = 3
        if send_status:
            box["status"] = 1 # ส่งแล้ว
        elif not send_status:
            box["status"] = 0 # ยังไม่ได้ส่ง
        if send_by:
            if send_by == "รอครูอนุมัติ":
                box["sendby"] = 0 # รอครูอณุมัติ
            else:
                box["sendby"] = 1 # อนุมัติแล้ว
    print(box)
    response_date = json.dumps(box)
    client_socket.send(response_date.encode('utf-8'))
    print("Received:", data.decode('utf-8'))

client_socket.close()
server_socket.close()