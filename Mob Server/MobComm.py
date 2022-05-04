from socket import *
import pandas as pd

'''
Reads dataset and split for induction 1 and induction 2 seperately
'''
dataset = pd.read_excel('SampleData.xlsx')
dataset = dataset.iloc[:,:3]

dataset_induction_1 = dataset[dataset['Induct Station']==1]
dataset_induction_2 = dataset[dataset['Induct Station']==2]

col_1 = 0
col_2 = 0


'''
socket communication to connect server
'''
sock_obj = socket()
sock_obj.connect(('192.168.43.9',7766))

'''
1,1 => induction 1 & bot 1
1,2 => induction 1 & bot 2
2,1 => induction 2 & bot 1
2,2 => induction 2 & bot 2
'''

while 1:
	a,b = map(input().split(','))

	if a==1:
		dest = dataset_induction_1.iloc[col_1]['Destination']
		col_1+=1
	else:
		dest = dataset_induction_2.iloc[col_2]['Destination']
		col_2+=1

	msg = '{},bot{}'.format(dest,b)		# msg format Ex; 'Pune,bot1'
	sock_obj.send(msg.encode())			#sends msg to system server

sock_obj.close()
