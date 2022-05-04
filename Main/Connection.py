from socket import *
import PublicVal

class Connection():

	def __init__(self):
		self.host    = PublicVal.host       # host is mention in PublicVal.py as a common value
		self.port    = PublicVal.port       # port is mention in PublicVal.py as a common value 
		self.BOTSIZE = PublicVal.BotSize    # BotSize is mention in PublicVal.py as a common value
		self.Start_tcp_Connection()

	def Start_tcp_Connection(self):
		self.sock_obj = socket(AF_INET, SOCK_STREAM)  # socket server creation
		self.sock_obj.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.sock_obj.bind((self.host, self.port))   # socket server bind socket address (host and port number)
		self.sock_obj.listen(2)  # socket server listening

		print ('[+] TCP Server Start !')
		for _ in range(self.BOTSIZE):
			conn_obj, addr = self.sock_obj.accept()  # server connection establishment

			'''
			In some case, bot are connected with different delay time, 
			example:
			     bot2 is connected , bot1 is connected

			     In this case connection object may be collision

			     So, Bot is when connecting this server ,its sends own name like bot1, bot2 , etc.,  
			'''
			BotName = conn_obj.recv(1024).decode().strip()  

			print ('[+] BotName : {} => {}:{}'.format(BotName, addr[0], addr[1]))

			'''
			All the connection objects are stores common value like JSON format data in PublicVal.py.
			So, It can easily used when send controll signal from server to bot
			'''
			PublicVal.Bot_Details_JSON[BotName]['ConnObj'] = conn_obj

	def Stop_tcp_Connection(self):
		for conn_obj in self.ConnObjList:
			conn_obj.close()
		self.sock_obj.close()
