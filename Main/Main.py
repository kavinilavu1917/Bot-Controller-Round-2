'''
Connection module used to Bot connections
PublicVal module used to access common value of all threads communication with it
FrontFrame module used to display path movements with CHESS BOARD shaped GUI
'''
from Connection import Connection
import PublicVal
from threading import Thread
from FrontFrame import FrontFrame


'''
	This Main Class used to connect All the Bot Connect's with 
	Socket using given host and port number 9488.
'''
class Main():

	def __init__(self):
		self.Connection_Class_obj = Connection()


if __name__ == '__main__':
	'''
	This PublicVal.init() used to start of a process with initialization
	common values  
	'''
	PublicVal.init()

	'''
	This Thread used to connect Mobile. In this case, we can not use any mobile apps.
	We use anthor socket programming in another systems.
	It is used to gives a signal of which  Bot is move and which is the destinaion 

	Signale -> botname, destination place
	'''
	Thread(target=PublicVal.ConnectMob,daemon=True).start()


	'''
	This Thread used to connect All given Bots in daemon threading.
	Usually ,its not required in thread.
	But, In this case we use this thread because, we communicate more than one autobots
	so, The Connection will be connect some difference various time.
	Front Frame GUI opens some time. so, its used to reduce timing to overcome it
	'''
	Thread(target=Main,daemon=True).start()

	'''
	This used to display Path Structure Board LIKE CHESS BOARD feature
	'''
	FrontFrame()

	#print (PublicVal.PathStructure, PublicVal.destination)

	#this is used to terminate all connections
	PublicVal.Stop()