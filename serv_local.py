#!/usr/bin/python3
import socket
import threading
import json
import time

HOST = socket.gethostbyname('localhost')
#HOST = '10.24.6.40'
PORT = 3000

ss_tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ss_tcp.bind((HOST,PORT))
ss_tcp.listen(9999)

client_all = set()
clients={}
data=time.asctime().split(' ')
data='_'.join(data)
arq=open(data+'.log','w')

def coloringClient (msg):
	msg = '\033[32m'+msg+'\033[0m'
	return msg

def sendingClient (msg,client):
	byte_msg = coloringServ(msg).encode('utf-8')
	client.send(byte_msg)

def coloringServ (msg):
	msg = '\033[34m'+msg+'\033[0m'
	return msg

def sendingServ (msg,client):
	byte_msg = coloringServ(msg).encode('utf-8')
	client.send(byte_msg)
		
def chat (client, addr):
	message = "SERV ---> Qual o seu nome?"
	sendingServ(message,client)

	nome = client.recv(1024)
	nome = nome.decode('utf-8')

	if not nome:
		client.close()
	elif nome=="$$QUIT": client.close()
	else:
		clients[addr]=nome
		message = nome + ' entrou!'
		arq.write(time.asctime()+': '+message+'\n')
		for c in client_all:
			sendingServ(message,c)
		entrance = 'SERV ---> Usuarios online -  %s'%(list(clients.values()))
		sendingServ(entrance,client)

	while True:
		message = client.recv (1024)
		byte_msg = message.decode('utf-8')
		if byte_msg=="$$QUIT":
			x=3
			while x > 0:
				exiting = 'SERV ---> Desconectando em %ds'%x
				sendingServ(exiting,client)
				time.sleep(1)
				x-=1
			client.close()
			client_all.remove(client)
			message = clients[addr] + ' saiu!'
			arq.write(time.asctime()+': '+message+'\n')
			del clients[addr]
			for l in client_all:
				sendingServ(message,l)
			break
		elif byte_msg == '$$VIEW_ALL':
			allon ='SERV ---> Usuarios online: %s'%(list(clients.values()))
			arq.write(time.asctime()+': '+allon+'\n')
			sendingServ(allon,client)
		elif not byte_msg:
			continue
		else:
			message = clients[addr] + ' ---> ' + byte_msg
			arq.write(time.asctime()+': '+message+'\n')
			for x in client_all:
				sendingClient(message,x)

while True:
	client, addr = ss_tcp.accept()
	client_all.add(client)
	t = threading.Thread(target = chat,args = tuple([client,addr]))
	t.start()

arq.close()
ss_tcp.close()
