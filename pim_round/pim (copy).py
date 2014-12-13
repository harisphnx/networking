import sys
import time
import random
from random import randint
import turtle
from turtle import *
import numpy as np
import math

### Get the cursor position to the correct position###
def setPos(turt,back,up):
	turt.up()
	turt.back(back)
	turt.left(90)
	turt.forward(up)
	turt.down()
	
def drawcicle(n,val):
	tlist = list()
	screen = turtle.getscreen()
	screen.tracer(0)
	for i in range(n):
	    	tlist.append(turtle.Turtle())
		setPos(tlist[i],val,200-(10+90*i))
		tlist[i].begin_fill()
		tlist[i].circle(15)
		tlist[i].end_fill()
		tlist[i].hideturtle() 
	for i in range(n):
	    	turt = turtle.Turtle()
		setPos(turt,val-300,200-(10+90*i))
		turt.begin_fill()
		turt.circle(15)
		turt.end_fill() 
		turt.hideturtle()
	screen.update()

def drawVOQ(n,val):
	tlist = list()
	screen = turtle.getscreen()	
	screen.tracer(0)
	count = 0 
	for i in range(n):
		for j in range(n):
	  	  	tlist.append(turtle.Turtle())
			setPos(tlist[count],val+5,210-(10+90*i+j*10))
			if j in voqList[i]:
				tlist[count].begin_fill()
			for k in range(2):
				tlist[count].forward(7)
				tlist[count].left(90)
				tlist[count].forward(30)
				tlist[count].left(90)
			if j in voqList[i]:
				tlist[count].end_fill()
			tlist[count].hideturtle() 
			count += 1
	screen.update()

def initialiseDraw(array,n,isGrant,val):
	x = list()
	y = list()
	count = 0
	acceptCount = 0
	for i in range(n):
		for j in range(n):
			if array[i][j] == 1:
				x.append(10+i*90)
				y.append(10+j*90)
				count+=1
	
	if isGrant == 0:
		suf = 0
		acceptCount = count+1
		for i in range(n):
			for j in range(n):
				acceptance[i][j]=0
				if(sending[i][j] == 1 and suf < speedup_factor):	#acceptance = [[0 for j in range(n)] for i in range(n)]
					x.append(10+i*90)
					y.append(10+j*90)
					count += 1
					sending[i][j]=0
					suf += 1
					voqList[i].remove(j)
				#acceptance[i].remove(j)
		drawVOQ(n,600)	
	if isGrant == 1:
		draw(y,x,count,1,val,acceptCount)
	else:
		draw(x,y,count,isGrant,val,acceptCount)

def drawText(text,back,up):
	screen = turtle.getscreen()
	turt = turtle.Turtle()
	screen.tracer(0)
	setPos(turt,back,up)
	turt.write(text,font=("Comin Sans MS", 20, "normal"))
	turt.hideturtle()
	screen.update()
def draw(x,y,count,isGrant,val,acceptCount):
	tlist = list()
	p = list()
	screen = turtle.getscreen()
	screen.setup( width = 2000, height = 2000, startx = None, starty = None) 
	for i in range(count):
	    screen.tracer(10)
	    tlist.append(turtle.Turtle())
	    #print "here",i,acceptCount,count
	    tlist[i].color("red")
	    if i >= acceptCount-1 and acceptCount!= 0:
		tlist[i].shape("square")
	    	tlist[i].color("green")
	    tlist[i].speed(1)
	    tlist[i].width(4)
	    angle = math.atan((y[i]-x[i])/300.0)
	    p.append(math.sqrt(90000+(x[i]-y[i])*(x[i]-y[i])))
	    if val == 200:
		setPos(tlist[i],val-275,200-x[i])
	    else:
		setPos(tlist[i],val,200-x[i])
	    if isGrant == 1:
		    tlist[i].right(180-math.degrees(angle)+90)
	    else:
		    tlist[i].right(math.degrees(angle)+90)
	    screen.update()
    
	for i in xrange(100):
		j=0
		for t in tlist:
			t.down()
			if (i*(i+1))/2 < p[j]:
				t.forward(i)
			j=j+1
		screen.update()

n = int(raw_input("Enter the number of port \n"))
speedup_factor = int(raw_input("Enter the speed up factor "))
acceptance = [[0 for j in range(n)] for i in range(n)]
sending = [[0 for j in range(n)] for i in range(n)]
voqList = [[] for i in range(n)]
request = [[0 for j in range(n)] for i in range(n)]
accept = [[0 for j in range(n)] for i in range(n)]
temp_list = []
flag = 0
send_count = 0

for i in range(n):
        for j in range(n):
                temp = (randint(0,100) % 2)
                request[i][j] = temp
                if(temp == 1):
                        voqList[i].append(j)

temp_list = []
print request
temp = 0
iteration = 1
while(flag == 0):
	flag = 1
	print "*************ITERATION ",iteration,"*************"
	if iteration == 1:
		drawText("REQUEST",550,225)
	else:
		drawText("REQUEST AND SENDING",550,225)
		send_count -= speedup_factor
	drawcicle(n,550)
	for i in range(n):
		for j in range(n):
			if(request[i][j] == 1):
				print "voq",i+1,"sends request to output",j+1
		print "\n"
	print "-----------------------------------------"
	initialiseDraw(request,n,0,550)	
	for i in range(n):
		for j in range(n):
			if(request[j][i] == 1):
				temp_list.append(j)
		count = len(temp_list)
		if(count > 0):
			temp = random.randint(0,count-1)
			accept[temp_list[temp]][i] = 1
			print "output",i+1,"send grant to",temp_list[temp]+1
		temp_list = []
	drawText("GRANT",100,225)
	drawcicle(n,125)
	drawVOQ(n,175)
	initialiseDraw(accept,n,1,-150)
	
	drawText("ACCEPT",-350,225)
	drawcicle(n,-300)
	drawVOQ(n,-250)
	print "-----------------------------------------"
	for i in range(n):
	        for j in range(n):
	                if(accept[i][j] == 1):
	                        temp_list.append(j)
				accept[i][j] = 0
	        count = len(temp_list)
	        if(count > 0):
		        temp = random.randint(0,count-1)
		        print "input",i+1,"send accept to",temp_list[temp]+1
			acceptance[i][temp_list[temp]] = 1
			sending[i][temp_list[temp]] = 1
			send_count += 1
			flag = flag + 1
			for x in range(n):
				request[i][x] = 0
				request[x][temp_list[temp]] = 0
	        temp_list = []
	initialiseDraw(acceptance,n,2,-300)	
        for i in range(n):
                for j in range(n):
                        if(request[i][j] == 1):
				flag = 0
	iteration = iteration + 1
	turtle.exitonclick()
while(send_count > 0):
	drawText("SENDING",550,225)
	drawcicle(n,550)
	send_count -= speedup_factor
	initialiseDraw(request,n,0,550)	
	turtle.exitonclick()
