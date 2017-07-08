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

def chat (client, addr):
	message = '\033[34m'+"SERV ---> Qual o seu nome?"+'\033[0m'
	byte_msg = message.encode('utf-8')
	client.send(byte_msg)

	nome = client.recv(1024)
	nome = nome.decode('utf-8')

	if not nome:
		client.close()
	elif nome=="$$QUIT": client.close()
	else:
		clients[addr]=nome
		message = '\033[34m'+nome + ' entrou!'+'\033[0m\n'
		arq.write(time.asctime()+': '+message+'\n')
		byte_msg = message.encode('utf-8')
		for c in client_all:
			c.send(byte_msg)
		entrance = '\033[34m'+'SERV ---> Usuarios online -  %s'%(list(clients.values()))+'\033[0m'
		entrance = entrance.encode('utf-8')
		client.send(entrance)

	while True:
		message = client.recv (1024)
		byte_msg = message.decode('utf-8')
		if byte_msg=="$$QUIT":
			x=3
			while x > 0:
				exiting = '\033[34m'+'SERV ---> Desconectando em %ds'%x+'\033[0m'
				exiting = exiting.encode('utf-8')
				client.send(exiting)
				time.sleep(1)
				x-=1
			client.close()
			client_all.remove(client)
			message = '\033[34m'+'SERV ---> ' + clients[addr] + ' saiu!'+'\033[0m'
			arq.write(time.asctime()+': '+message+'\n')
			message = message.encode('utf-8')
			del clients[addr]
			for x in client_all:
				x.send(message)
			break
		elif byte_msg == '$$VIEW_ALL':
			allon = '\033[34m'+'SERV ---> Usuarios online: %s'%(list(clients.values()))+'\033[0m'
			arq.write(time.asctime()+': '+allon+'\n')
			allon = allon.encode('utf-8')
			client.send(allon)
		elif not byte_msg:
			continue
		else:
			message = '\033[32m'+clients[addr] + ' ---> ' + byte_msg+'\033[0m'
			arq.write(time.asctime()+': '+message+'\n')
			message = message.encode('utf-8')
			for x in client_all:
				x.send(message)

while True:
	client, addr = ss_tcp.accept()
	client_all.add(client)
	t = threading.Thread(target = chat,args = tuple([client,addr]))
	t.start()

arq.close()
ss_tcp.close()
