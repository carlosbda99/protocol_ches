#!/usr/bin/python3
import socket
import threading
import time

HOST = socket.gethostbyname('localhost')
PORT = 3000

ss_tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ss_tcp.bind((HOST,PORT))
ss_tcp.listen(9999)

client_all = set()
clients={}
private={}
data=time.asctime().split(' ')
data='_'.join(data)
arq=open(data+'.log','w')

def coloringClient (msg):
	msg = '\033[32m'+msg+'\033[0m'
	return msg

def sendingClient (msg,client):
	byte_msg = coloringClient(msg).encode('utf-8')
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
	elif nome in list(clients.values()): 
		sendingServ('Nome ja utilizado por um usuario on line...\n',client)
		chat(client,addr)
	else:
		if nome=="$quit": client.close()
		private[nome]=client
		clients[addr]=nome
		message = nome + ' entrou!\n'
		arq.write(time.asctime()+': '+message)
		for c in client_all:
			sendingServ(message,c)
		entrance = 'SERV ---> Usuarios online -  %s'%(list(clients.values()))
		entrance= entrance + '\n"$man" = Manual de comandos'
		sendingServ(entrance,client)

		while True:
			message = client.recv (1024)
			byte_msg = message.decode('utf-8')
			if byte_msg=="$quit":
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
				del private[nome]
				del clients[addr]
				for l in client_all:
					sendingServ(message,l)
				break
			elif byte_msg == '$allonline':
				allon ='SERV ---> Usuarios online: %s'%(list(clients.values()))
				sendingServ(allon,client)
			elif byte_msg.split(' ')[0] == '$private':
				if byte_msg.split(' ')[1] not in list(clients.values()):
					msg = 'SERV ---> USUARIO NAO CONECTADO'
					sendingServ(msg,client)
					break
				elif byte_msg.split(' ')[1] == nome:
					msg = 'SERV ---> IMPOSSIVEL ENVIAR PARA SI MESMO'
					sendingServ(msg,client)
					break
				amsg = byte_msg.split(' ')
				msg = ' '.join(amsg[2:])
				msg = nome + ' --$> ' + msg
				arq.write(time.asctime() + ': ' + msg + ' para ' + amsg[1] + '\n')
				sendingClient(msg,private[amsg[1]])
			elif byte_msg=='$man':
				msg = '"$quit" = Sair do bate-papo\n"$allonline" = Visualisar usuarios online\n"$private <nome_usuario_destino> <mensagem> = Envia <mensagem> para <nome_usuario_destino>"'
				sendingServ(msg,client)
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
