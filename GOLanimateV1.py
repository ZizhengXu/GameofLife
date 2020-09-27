# coding=gb2312
import numpy as np
import time
import matplotlib.pyplot as plt
import os

def disp(top):
	global fig,wst,fd,WorldSize,count_text
	plt.clf()
	ax=fig.add_subplot(111)
	i=ax.imshow(np.transpose(wst),interpolation='nearest',origin='lower')
	fig.colorbar(i)
	plt.scatter( x[:top],y[:top],c='g',s=np.array(fd)/6,linewidths=0.1,edgecolors='k')
	plt.xlim((0,WorldSize))
	plt.ylim((0,WorldSize))
	plt.title('count = %d' % top)

def ini():
	global InitialCells,mr
	InitialCells=10
	mr=30
	global WorldSize
	WorldSize=100
	global top
	top=InitialCells
	global dx,dy
	dx=[0 for i in range(InitialCells)]
	dy=[0 for i in range(InitialCells)]
	global x
	x=[np.random.randint(0,WorldSize) for i in range(InitialCells)]
	""" establish and innitialize an array"""
	global y
	y=[np.random.randint(0,WorldSize) for i in range(InitialCells)]
	global fd
	fd=[70 for i in range(InitialCells)]
	global wst
	wst=np.random.poisson(10.,(WorldSize,WorldSize))
	global fig
	fig=plt.figure()
	plt.plot(x[:top],y[:top],'ro')
	ax=fig.gca()
	i=ax.imshow(wst,interpolation='nearest')
	fig.colorbar(i)
	global count_text
	# count_text = ax.text(-0.2, -1.5, '', transform=ax.transAxes)
	# plt.show()


def decide2(curr):
	[dx1,dx2,dy1,dy2]=[0,0,0,0]
	##print(dx1,dx2,dy1,dy2) the last sentence is valid
	global wst,sunshine,x,y,dx,dy
	bnft1=-100
	for i in range(-1,2):
		for j in range(-1,2):
			if (x[curr]+i>=0)and(x[curr]+i<WorldSize)and(y[curr]+j>=0)and(y[curr]+j<WorldSize):
				tmp=-wst[x[curr]+i][y[curr]+j]+sunshine[x[curr]+i][y[curr]+j]
				if tmp>bnft1:
					bnft1=tmp
					dx1=i
					dy1=j

	bnft2=-100
	for i in range(-1,2):
		for j in range(-1,2):
			if (x[curr]+i>=0)and(x[curr]+i<WorldSize)and(y[curr]+j>=0)and(y[curr]+j<WorldSize)and(i!=dx1)and(j!=dy1):
				tmp=-wst[x[curr]+i][y[curr]+j]+sunshine[x[curr]+i][y[curr]+j]
				if tmp>bnft2:
					bnft2=tmp
					dx2=i
					dy2=j
	# if the environment is unfavorable, no fission
	if (bnft1<-40)or (bnft2<-40):dx[curr]=0;dy[curr]=0;return()
	# fission
	dx[curr]=dx2
	dy[curr]=dy2
	fd[curr]/=2
	global top
	top+=1
	dx.append(0)
	dy.append(0)
	fd.append(fd[curr])
	x.append(x[curr]+dx1)
	y.append(y[curr]+dy1)

def decide ():
	global top,fd,dx,dy,x,y,wst,sunshine
	top1=top
	for curr in range(top1):
		if fd[curr]>=80 :
			decide2(curr)
		else:
			bnft=-100
			dx[curr]=0
			dy[curr]=0
		#	print(curr)
			for i in range(-1,2):
				for j in range(-1,2):
					if (x[curr]+i>=0)and(x[curr]+i<WorldSize)and(y[curr]+j>=0)and(y[curr]+j<WorldSize):

						tmp=-wst[x[curr]+i][y[curr]+j]+sunshine[x[curr]+i][y[curr]+j]
						if tmp>bnft:
							bnft=tmp
							dx[curr]=i
							dy[curr]=j


def move(curr):
	if dx[curr]==0 or dy[curr]==0 :return 0
	else: return 10
def LogOff(curr):
	global top,x,y,fd
	del x[curr]
	del y[curr]
	del fd[curr]
	del dx[curr]
	del dy[curr]
	top-=1
def refresh():
	global top
	global wst
	global x
	global y
	global fd,WorldSize,mr
	CD=[[0 for i in range(WorldSize)]for  i in range (WorldSize)]#Cell distribution
	for curr in range(top):
		wst[x[curr]][y[curr]]+=mr############_____motabolism rate
		x[curr]+=dx[curr]
		y[curr]+=dy[curr]
		CD[x[curr]][y[curr]]+=1
	curr=0
	while curr<top:
		fd[curr]+=(sunshine[x[curr]][y[curr]]/CD[x[curr]][y[curr]]-wst[x[curr]][y[curr]]-move(curr))
		if fd[curr]<0 :
			LogOff(curr)
			curr-=1
		curr+=1

#from math import log
import matplotlib.animation as animation
ini()
#import os
timespan=100
t=0

import scipy.ndimage as ndimage  #################for guassian filter

def sc(x):
	if x<6:	return x 
	else:return (x**(0.9)+1)
def animate(_):
	global sunshine
	sunshine=np.random.randint(15,40+1,size=(WorldSize,WorldSize))
	decide()
	refresh()
	global wst
	for i in range (WorldSize):
		for j in range(WorldSize):
			wst[i][j]=round(sc(wst[i][j]))
#########################  self-cleaning function here #########################

	wst=ndimage.gaussian_filter(wst, sigma=0.21, order=0)
	global top
	disp(top)
	print('  ',top)
	# if top==0:
	# 	import os
	# 	os.system("pause")
		# time.sleep(2)

for i in range(100):
	ani = animation.FuncAnimation(fig, animate )
	#os.system("pause")

plt.show()

