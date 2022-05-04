import time
import sys
import cv2
import PublicVal
from ImageAgumentation import ImageAgumentation 
from PathRegressor import PathRegressor
import requests
from BotPlaceFinder import BotPlaceFinder
from threading import Thread
from shapely.geometry import *

'''
This is used for Controll All bots in Threading process
Its leads to gets movement using 
	=> bot angle, bot center
	=> bot predicted path
	=> connection object to send socket communication

Mechanism:
	-> Bot angle and Bot center are gets from ImageAgumentation using Aruco
	   with different given ID
	-> bot path prediction using PathRegressor
	-> communication between bot and system maintainance

Connection Object Commands:

	L -> Left
		Those decides angle variance between bot center and dest center
			X -> Low Left
			Y -> Medium Left
			Z -> High Left

	R -> Right
		Those decides angle variance between bot center and dest center
			X -> Low Right
			Y -> Medium Right
			Z -> Hight Right

	F -> Forward
		Those decides distance variance between bot center and dest center
			X -> Low Forward
			Y -> Medium forward
			Z -> Hight Forward
'''


class Controll: 
	def __init__(self,BotName,dest_place):
		'''
		Basic Requirements :
			=> Bot name
			=> Connection object for socket communication
			=> Aruco ID to determine angle, center
			=> Destination place
		'''
		self.BotName  = BotName
		self.conn_obj = PublicVal.Bot_Details_JSON[BotName]['ConnObj']
		self.ID       = PublicVal.Bot_Details_JSON[BotName]['ID']

		self.dest_place=dest_place
		self.Forward=False


		'''
		This steps used to find a bot which is placed in nearest Induction place
		place -> index position in 14x14 matrix
		'''
		while 1:
			try:
				angle, center   = ImageAgumentation().ArucoAgumentation(PublicVal.Image, self.ID)			
				if angle!=None and center!=None:
					break
				else:
					#print ('aruco not detect')
					time.sleep(1)
			except:
				#print ('aruco not detected!')
				time.sleep(1)
		Induction_point = self.Manhatten_Distimatic_Point(center)

		self.BotPlace   = Induction_point  # set induction place as Bot place 
		PublicVal.PathStructure[self.BotPlace[0]][self.BotPlace[1]]=1 # define 1 in pathstructure

		self.Forward=True

		# Bot Movement Path Controll Establishment 
		self.BotPathEstablishment()


		'''
		Bot deliverd Successfully!
		Then next move is return  nearest Induction Postion
		So, We find nearest Induction postion using those method
		Nearest Induction postion set as a destination postion
		'''
		angle,center = ImageAgumentation().ArucoAgumentation(PublicVal.Image,self.ID)
		self.Forward=False
		while 1:
			angle, center   = ImageAgumentation().ArucoAgumentation(PublicVal.Image, self.ID)			
			if angle!=None and center!=None:
				break
			else:
				#print ('aruco not detected')
				time.sleep(1)
		Induction_point = self.Manhatten_Distimatic_Point(PublicVal.center_array[self.BotPlace[0],self.BotPlace[1],0])
		self.dest_place=[Induction_point]



		# Bot Movement path controll establishment
		self.BotPathEstablishment()

		# It holds path place in pathstructure
		PublicVal.PathStructure[self.BotPlace[0]][self.BotPlace[1]]=1
		self.Forward=True

		'''
		It is a important one function.
		Because, its uses terminating Thread. So , the process of execution increase this function
		'''
		sys.exit()


	def Manhatten_Distimatic_Point(self,center):
		'''
		Manhatten Distance
		Formula:
			Distance between (x1, y1) and (x2, y2)

			distance = | x1 - y1 | + | x2 - y2 |
		'''
		induction1 = abs(center[0]-PublicVal.center_array[4,0,0,0]) + abs(center[1]-PublicVal.center_array[4,0,0,1])
		induction2 = abs(center[0]-PublicVal.center_array[9,0,0,0]) + abs(center[1]-PublicVal.center_array[9,0,0,1])
		if induction1>induction2:
			return (9,0,)
		else:
			return (4,0,)

	def find_distance_between_two_points(self,point1,point2):
		'''

		Formula :
			Distance between (x1, y1) and (x2,y2)

			distance = Square_root_of( (x1-x2)^2 + (y1-y2)^2)
		'''
		return round(((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2 )**0.5)

	def PolygonPointTest(self,CenterPoint, EdgePoint):
		'''
		This function used to find a bot center point with in that closed edge point or not
		'''
		point=Point(CenterPoint)
		polygon=Polygon(EdgePoint)
		return polygon.contains(point)


	def MoveMentControlling(self,dest_center, dest_edge):
		'''
		This function Controlls Bot Movement with Socket Communication

		Machanism:
			=> Detect angle, center of a bot
			=> Destination require rotation angle detection
			=> Checks a bot is placed on next place or not
				If its not:
					$ sends a signal of commands to move a bot
						> send movement signal (F, L, R)
						> send delay signal (X, Y ,Z)
						> receives ACK
				else:
					$ Return True (That's shows terminate this function) 

			=> It have a controll flag:
				$ It avoids bot displacement
		'''
		current_edge = PublicVal.edge_array[self.BotPlace[0], self.BotPlace[1], 0]
		print ('Destination ',dest_center)
		while 1:
			Image_Obj    = ImageAgumentation()
			angle,center = Image_Obj.ArucoAgumentation(PublicVal.Image, self.ID)
			if angle==None and center==None:
				#print ('[-] Aruco is not Detected')
				time.sleep(1)
				continue

			angleNum     = Image_Obj.PointAgumentation(center,dest_center)
			if self.PolygonPointTest(center, dest_edge):
				print("STOP")
				return True
			
			if not self.PolygonPointTest(center,current_edge):
				PublicVal.active_flag=False
				return False

			var = round(abs(angle-angleNum))
			var = min(var, 360-var)
			if PublicVal.active_flag:
				if var<11:
					self.conn_obj.send(b'F')
					dis = find_distance_between_two_points(center, dest_center)
					delay_command = PublicVal.ForwardVariance(dis).encode()
					self.conn_obj.send(delay_command)
					self.conn_obj.recv(1024).decode()
					#print("FORWARD")
				else:
					val = angleNum-angle
					if abs(val)<180:
						if val>0:
							self.conn_obj.send(b'R')
							delay_command = PublicVal.AngleVariance(var).encode()
							self.conn_obj.send(delay_command)
							self.conn_obj.recv(1024).decode()
							#print ('R ',angleNum,angle)
							#print("Right")
						elif val<0 :
							self.conn_obj.send(b'L')
							delay_command = PublicVal.AngleVariance(var).encode()
							self.conn_obj.send(delay_command)
							self.conn_obj.recv(1024).decode()
							#print ('L ',angleNum,angle)
							#print("Left")
					else:
						if val<0:
							self.conn_obj.send(b'R')
							delay_command = PublicVal.AngleVariance(var).encode()
							self.conn_obj.send(delay_command)
							self.conn_obj.recv(1024).decode()
							#print ('R ',angleNum,angle)
							#print("Right")
						elif val>0:
							self.conn_obj.send(b'L')
							delay_command = PublicVal.AngleVariance(var).encode()
							self.conn_obj.send(delay_command)
							self.conn_obj.recv(1024).decode()
							#print ('L ',angleNum,angle)
							#print("Left")
				
			

	def BotPathEstablishment(self):
		'''
			Its used to Predict shortest path
			Then, shows bot movements in GUI
		'''
		print_flag = True
		while 1:
			try:
				path = PathRegressor().Predict(PublicVal.PathStructure,self.BotPlace, self.dest_place)
				print (path)
				if path==None and print_flag:
					print ('[-] path become None!')
					print_flag=False
					continue
				print_flag=True
				if len(path)<=2 and self.Forward:
					break	
				oldx,oldy = self.BotPlace
				x,y = path[1]
				PublicVal.Label_List[oldx][oldy].config(text='1',background='red')
				PublicVal.Label_List[x][y].config(background='#0019fd')
				dest_center = PublicVal.center_array[x,y,0]
				dest_edge   = PublicVal.edge_array[x,y,0]
				if not self.MoveMentControlling(dest_center, dest_edge):
					self.BotPlace = BotPlaceFinder().place(self.BotName)
					PublicVal.active_flag=True
					continue
				PublicVal.Label_List[oldx][oldy].config(text='0',background='#37ff00')
				PublicVal.Label_List[x][y].config(text='1',background='red')
				self.BotPlace = path[1]
				PublicVal.PathStructure[oldx][oldy]=0
				PublicVal.PathStructure[x][y]=1

				if len(path)<=2 and not self.Forward:
					break
			except Exception as e:
				print ('{} {}'.format(self.BotName,e))
				break

		'''
		This is used to decides when Fliping is done!
		'''

		if self.Forward:
			self.FlipingTurn(path[-1],180)
			self.conn_obj.send(b'E')
			self.conn_obj.recv(1024).decode()
			print ('Flip')
			print ('Recived => ',self.conn_obj.recv(1024).decode())
			print ('Flipping Done!')
		else:
			self.FlipingTurn((self.dest_place[0][0]+1, self.dest_place[0][1]),0)
			print ('Settled Done!')

		
	def FlipingTurn(self,dest_center,error_angle):
		'''
		This Funtion used to done a fliping controll of in given angle
		'''
		while 1:
			try:
				Image_Obj    = ImageAgumentation()
				angle,center = Image_Obj.ArucoAgumentation(PublicVal.Image, self.ID)
				if angle==None and center==None:
					print ('[-] Aruco is not Detected')
					time.sleep(1)
					continue
				angleNum     = Image_Obj.PointAgumentation(center,dest_center) + error_angle
				angleNum     = angleNum%360
				var          = round(abs(angleNum-angle))
				var          = min(val,360-val)
				if var<11:
					print("STOP")
					break
				else:
					val = angleNum - angle
					if abs(val)<180:
						if val>0:
							self.conn_obj.send(b'R')
							delay_command = PublicVal.AngleVariance(var).encode()
							self.conn_obj.send(delay_command)
							self.conn_obj.recv(1024).decode()
							#print ('R ',angleNum,angle)
							#print("Right")
						elif val<0:
							self.conn_obj.send(b'L')
							delay_command = PublicVal.AngleVariance(var).encode()
							self.conn_obj.send(delay_command)
							self.conn_obj.recv(1024).decode()
							#print ('L ',angleNum,angle)
							#print("Left")
					else:
						if val<0 :
							self.conn_obj.send(b'R')
							delay_command = PublicVal.AngleVariance(var).encode()
							self.conn_obj.send(delay_command)
							self.conn_obj.recv(1024).decode()
							#print ('R ',angleNum,angle)
							#print("Right")
						elif val>0:
							self.conn_obj.send(b'L')
							delay_command = PublicVal.AngleVariance(var).encode()
							self.conn_obj.send(delay_command)
							self.conn_obj.recv(1024).decode()
							#print ('L ',angleNum,angle)
							#print("Left")

			except Exception as e:
				print (e)
				break