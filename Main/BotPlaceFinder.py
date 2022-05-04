import numpy as np
from shapely.geometry import *
import PublicVal
from ImageAgumentation import ImageAgumentation
'''
This class is used to find which bot placed on 14x14 matrix 
And Return's it index position of 14x14 matrix
'''
class BotPlaceFinder:
	def place(self,botname):
		edgearray=PublicVal.edge_array
		ID = PublicVal.Bot_Details_JSON[botname]['ID']
		while 1:

			angle, center   = ImageAgumentation().ArucoAgumentation(PublicVal.Image, ID)			
			if angle!=None and center!=None:
				break
			else:
				#print ('aruco not detected')
				time.sleep(1)

		self.BotPlace=None
		for i in range(14):
			for j in range(14):
				edge = edgearray[i,j,0]
				if self.PolygonPointTest(center,edge):
					print (i,j)
					self.BotPlace=[i,j]
					break
		return self.BotPlace

	def PolygonPointTest(self,CenterPoint, EdgePoint):
		point=Point(CenterPoint)
		polygon=Polygon(EdgePoint)
		return polygon.contains(point)

