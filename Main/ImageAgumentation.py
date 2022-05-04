import cv2 
import cv2.aruco as aruco
import numpy as np
import math
import warnings
warnings.filterwarnings('ignore')

class ImageAgumentation:

	def getAngle(self,a, b, c):
		ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))+135
		ang = round(ang)
		return ang + 360 if ang < 0 else ang

	def ArucoAgumentation(self,img,ID):
		'''
		This function is used to Detect Aruco with dictionary of "DICT_4x4_250"
		which leads to get infromation about center point, angle with uniquily identified
		of a Aruco ID
		'''
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		key = getattr(aruco, f'DICT_4X4_250')
		arucoDict = aruco.Dictionary_get(key)
		arucoParam = aruco.DetectorParameters_create()
		bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
		Evaluation_Index = 0
		flag=False
		try:
			if ids.any():
				for i in range(ids.shape[0]):
					if ids[i,0]==ID:
						Evaluation_Index=i
						flag=True

				if flag:
					bbox_array = bboxs[Evaluation_Index]
					tr          = bbox_array[0,1,0],bbox_array[0,1,1]
					centerW     = float(bbox_array[0,2,0] - bbox_array[0,0,0])/float(2) + float(bbox_array[0,0,0])
					centerH     = float(bbox_array[0,2,1] - bbox_array[0,0,1])/float(2) + float(bbox_array[0,0,1])
					center      = int(centerW), int(centerH)
					angleFactor = int(centerW), int(centerH)+int(-100)
					angle       = self.getAngle(tr,center,angleFactor)
					return (angle,center)
				else:
					return (None, None)
			else:
				return None,None
		except AttributeError:
			return None,None

	def PointAgumentation(self, Bot_Center, Destination_Center):
		'''
		This Function used to get angle

		This machanism is

			=> Bot center is focused as a center of circle
			=> destination center is focused as a point of circle

		which leads to give an angle of bot center to destination center.

		That's uses to Bot rotation angle  
		'''
		Bot_Center = [Bot_Center[0],-Bot_Center[1]]
		Destination_Center = [Destination_Center[0], -Destination_Center[1]]

		try:
			slop = (Destination_Center[1] - Bot_Center[1]) / (Destination_Center[0] - Bot_Center[0])
			angle = math.atan(slop)*180/math.pi
		except ZeroDivisionError:
			angle=90

		if Bot_Center[0]<=Destination_Center[0] and Bot_Center[1]<=Destination_Center[1]:
			angle=angle 
		elif Bot_Center[0]<=Destination_Center[0] and Bot_Center[1]>=Destination_Center[1]:
			angle=360+angle
		elif Bot_Center[0]>=Destination_Center[0] and Bot_Center[1]>=Destination_Center[1]:
			angle=180+angle
		else:
			angle=180+angle
		return angle%360
