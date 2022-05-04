import cv2
import time,math
import center,sys
from socket import *
from threading import Thread
from Controll import Controll
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from skimage import transform
from skimage.io import imread,imshow

def init():

	'''
	This are the common value for all imported script / all imported programs
	'''
	global VideoCamera, host, port, BotSize, Bot_Details_JSON
	global PathStructure, destination,center_array,edge_array
	global conn_obj_list, Label_List,Image, active_flag
	global district_names,listen


	'''
	This is a controlling flag which is used to controll bot displacement in a square box.
	'''
	active_flag = True

	'''
	District name with uniqued scalar/integer/number
	'''
	district_names = {
		'Mumbai':1,
		'Delhi':2,
		'Kolkata':3,
		'Chennai':4,
		'Bengaluru':5,
		'Hyderabad':6,
		'Pune':7,
		'Ahmedabad':8,
		'Jaipur':9
	}

	'''
	This is a IP address / HOST address in our system
	'''
	host    = '192.168.43.9'

	'''
	This is used to capture video from our system.
	We are used IVCam application to connect mobile camera with system's camera using
	USB connector 
	'''
	VideoCamera = cv2.VideoCapture(0)

	'''
	This is used to get all 14x14 square's four edge points and center points for movement
	prediction
	'''
	edge_array,center_array = center.PathSplit(ImageResize(VideoCamera.read()[1]))

	'''
	This thread is used to retrieve common videocamera to image reader. All background
	process which needs a image, its provids properly. This technique reduces parallel camera
	access.

	Parrallel Camera access is a problem thats doesn't provides None images
	'''
	Thread(target=ReadImage, daemon=True).start()

	

	edge_array=np.array(edge_array)
	center_array=np.array(center_array)

	print ('[+] Edged and centers are detected! ')


	'''
	This a common value for all background bot information required process
	This is changeable.
	Some key features added in runtime environment
	'''
	Bot_Details_JSON = {
		'bot1':{
			'ID':12
		},
		'bot2':{
			'ID':2
		}
	}

	'''
	This is a PathStruction 14x14 matrix
	default 1 -> destination boxes 
	default 0 -> empty boxes

	In Runtime all bots are changed 0 to 1
	So, Bot location have 1 value at runtime excution

	This is used to predicting not colloide path
	'''

	PathStructure =[
		[0]*14,
		[0]*14,
		[0]*2 + [1]*2 + [0]*2 +[1]*2 +[0]*2 + [1]*2 +[0]*2,
		[0]*2 + [1]*2 + [0]*2 +[1]*2 +[0]*2 + [1]*2 +[0]*2,
		[0]*14,
		[0]*14,
		[0]*2 + [1]*2 + [0]*2 +[1]*2 +[0]*2 + [1]*2 +[0]*2,
		[0]*2 + [1]*2 + [0]*2 +[1]*2 +[0]*2 + [1]*2 +[0]*2,
		[0]*14,
		[0]*14,
		[0]*2 + [1]*2 + [0]*2 +[1]*2 +[0]*2 + [1]*2 +[0]*2,
		[0]*2 + [1]*2 + [0]*2 +[1]*2 +[0]*2 + [1]*2 +[0]*2,
		[0]*14,
		[0]*14
	]

	'''
	This is a destination index position of  14x14 matrix
	1-9 are the keys which leads to map a destination city name
	'''

	destination = {
		1:[(2,2),(2,3),(3,2),(3,3)],
		2:[(2,6),(2,7),(3,6),(3,7)],
		3:[(2,10),(2,11),(2,10),(3,11)],
		4:[(6,2),(6,3),(7,2),(7,3)],
		5:[(6,6),(6,7),(7,6),(7,7)],
		6:[(6,10),(6,11),(7,10),(7,11)],
		7:[(10,2),(10,3),(11,2),(11,3)],
		8:[(10,6),(10,7),(11,6),(11,7)],
		9:[(10,10),(10,11),(11,10),(11,11)]
	}


	'''
	port is a common value thats uses to connect a all bots with a common port.
	Multi Socket Communication leads this communicaiton establishmentations. 
	'''
	port    = 9488
	BotSize = 2     # Number of Bot's used

def ConnectMob():

	# This a common value for mobile client to system server communication
	global server_socket_obj,server_conn_obj
	

	'''
	This is used to connect Mobile client to this system server with same host and port number
	7766.
	'''
	server_socket_obj=socket(AF_INET,SOCK_STREAM)
	#server_socket_obj.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	server_socket_obj.bind((host,7766))
	server_socket_obj.listen(1)
	print ('[+] Start Mobile app connector server! ')
	server_conn_obj , addr = server_socket_obj.accept()
	print ('[+] Mobile app server Connected!')

	Thread(target=MobJsonRecv,daemon=True).start()

def MobJsonRecv():
	'''
	This is a important function for kickstart of bot controlling.
	Mobile Client sends a signal (botname, destination) when parcel is loaded
	in autobots.

	This function sends those information and leads a background threading
	process in Controll.py (Bot controlling script)
	'''
	JsonMessage=None
	while 1:
		JsonMessage = server_conn_obj.recv(1024).decode().strip().split(',')
		dest_place = destination[district_names[JsonMessage[1]]]
		botname    = JsonMessage[0].lower()
		Thread(target=Controll,args=(botname,dest_place,),daemon=True).start()


def ReadImage():
	'''
	This is a important function for accessing image processing , bot controlling.
	Because , its reads video camera images as a common variable.
	It's leads to which needs those image to execution

	And It's also provides Live Video Streaming
	'''
	global Image
	while 1:
		ret,img=VideoCamera.read()
		if ret:
			'''
			This function is very important bacause, Images were shown as a video camera
			perspective view. Its leads to wrap those images with equallity images
			'''
			Image = ImageResize(img)



			img          = cv2.resize(img,(642, 600))
			cv2.namedWindow('LiveVideo')
			cv2.imshow('LiveVideo',img)
			if cv2.waitKey(1)&0xff==ord('q'):
				break
	cv2.destroyAllWindows()
	sys.exit()



def Stop():
	'''
	Terminate all connections
	'''
	server_conn_obj.close()
	server_socket_obj.close()
	VideoCamera.release()
	cv2.destroyAllWindows()

def ImageResize(img):
	'''
	This function used to wrap a video camera images
	Mentions points of a array is a four edges of a required images to wrap
	'''
	height,width,_ = img.shape
	points=np.array([[950,5],[1178,677],[9,717],[204,43]]) # four edges of a image to wrap
	projections = np.array([[width,0],[width,height],[0,height],[0,0]])
	tform=transform.estimate_transform('projective',points,projections)
	tf_img_warp = transform.warp(img,tform.inverse,mode='symmetric')
	img=(tf_img_warp*255).astype('uint8')
	img = cv2.resize(img, (1500,1400),interpolation=cv2.INTER_LINEAR)
	return img

'''
X - > Low
Y - > Medium
Z - > High

'''


# Leads to give forward variance to delay timing controll
def ForwardVariance(dis):
	m=math.ceil(dis*3/100)
	return 'X' if m==1 else 'Y' if m==2 else 'Z'

# Leads to give Angle variance to delay timing controll
def AngleVariance(ang):
	m=math.ceil(ang*3/90)
	return 'X' if m==1 else 'Y' if m==2 else 'Z'