import PublicVal
from tkinter import *
from tkinter import ttk 
from PIL import ImageTk, Image
from datetime import datetime
import time,sys
import platform
from PIL import Image, ImageOps
from threading import Thread
import cv2 
'''
This class used to display path movement in Graphical User Interface mode.
That's leads to easily identify bot path

We use only shows a next position. Because, In more than one Bots case,
we can't using static path. So, we use dynamic path. so We can use only shows
a next position of bot and current position of a bot

1,0 are value of PathStructure (PublicValue.py) (common value)
'''
class FrontFrame:
	def __init__(self):
		self.root_obj              = Tk()
		self.panedwindow2          = ttk.Panedwindow(self.root_obj,orient=HORIZONTAL)
		self.panedwindow2.pack()
		self.Frame1                = Frame(self.panedwindow2,width=500,height=500,relief=SUNKEN)
		self.canvas_obj            = Canvas(self.Frame1, width=500,height=500,background='#ede4aa')
		self.canvas_obj.place(x=10,y=10)
		self.label_list            = []
		self.default_color=[]
		self.detection_index=[]
		for i in range(1,15):
			labels = []
			colr=[]
			for j in range(1,15):
				if PublicVal.PathStructure[i-1][j-1] == 0:
					self.detection_index.append((i-1,j-1))
					color = '#37ff00'
				else:
					color = '#00ffdd'
				colr.append(color)
				l = Label(self.canvas_obj,text=f'{PublicVal.PathStructure[i-1][j-1]}',padx=5,font=('Helvetica bold',20),fg='#030303',background=color)
				l.place(x=30*j,y=30*i)
				labels.append(l)
			self.label_list.append(labels)
			self.default_color.append(colr)
		PublicVal.Label_List=self.label_list
		self.panedwindow2.add(self.Frame1, weight=1)
		self.root_obj.mainloop()