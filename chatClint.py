#!/usr/bin/python3
import socket
import threading

HOST = socket.gethostbyname('localhost')
PORT = 3001

cs_tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

cs_tcp.connect((HOST,PORT))

serv_quest = cs_tcp.recv(1024)
serv_quest = serv_quest.decode('utf-8')
print (serv_quest)
nome=''

def listening (HOST,PORT):
    while True:
        line = cs_tcp.recv(1024)
        line = line.decode('utf-8')
        if(line.count(nome+' entrou!')):
            print (line.replace(nome,'Voce',1))
        else: 
            print (line)

while True:
    message = input()
    if nome == '':
        nome=message
    message = message.encode('utf-8')
    cs_tcp.send(message)
    t = threading.Thread(target = listening, args = (HOST,PORT))
    t.start()
