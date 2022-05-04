import cv2
from matplotlib import pyplot as plt 
import numpy as np
from skimage import transform
from skimage.io import imread,imshow

def mid(x,y,x1,y1):
	mid_x=(x+x1)//2
	mid_y=(y+y1)//2
	return int(mid_x),int(mid_y)

def PathSplit(img):
	corners=[]
	mids=[]
	width,height,_=img.shape
	print(width,height)
	value=100
	print(value)
	start_x=value
	start_y=0
	end_x=value+value
	end_y=value
	for i in range(1,15):
		if(i!=1):
			start_y+=value
			end_y+=value
			start_x=value
			end_x=value+value
		for j in range(1,15):
			temp=[]
			temp.append(int(start_x+value))
			temp.append(int(start_y))
			temp.append(int(end_x))
			temp.append(int(end_y))
			temp.append(int(end_x-value))
			temp.append(int(end_y))
			temp.append(int(start_x))
			temp.append(int(start_y))
			corners.append(temp)
			# print(start_x,start_y,end_x,end_y)
			a=mid(start_x+value,start_y,end_x-value,end_y)
			mids.append(a)
			cv2.putText(img,',',(int(start_x+value),int(start_y)),cv2.FONT_HERSHEY_SIMPLEX,2,(255, 0, 0),2)
			cv2.putText(img,'.',(int(end_x-value),int(end_y)),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),2)
			cv2.putText(img,'.',a,cv2.FONT_HERSHEY_SIMPLEX,2,(255,250,0),2)
			start_x+=value
			end_x+=value

	mids = np.array(mids).reshape(14,14,1,2)
	edge = np.array(corners).reshape(14,14,1,4,2)
	return edge, mids
