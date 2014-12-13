import sys
import turtle
from turtle import *
import numpy as np
import math
import time
import random
from random import randint
from route_lookup import *

#################### put the turtle to correct position #####################
	
def Start_Draw(x,y,count,isGrant,val,acceptCount):
	List_Of_Turtles = list()
	p = list()
	screen = turtle.getscreen()
	screen.setup( width = 2000, height = 2000, startx = None, starty = None) 
	for i in range(count):
	    screen.tracer(10)
	    List_Of_Turtles.append(turtle.Turtle())
	    #print "here",i,acceptCount,count
	    List_Of_Turtles[i].color("blue")
	    if i >= acceptCount-1 and acceptCount!= 0:
		List_Of_Turtles[i].shape("square")
	    	List_Of_Turtles[i].color("green")
	    List_Of_Turtles[i].speed(1)
	    List_Of_Turtles[i].width(3)
	    angle = math.atan((y[i]-x[i])/300.0)
	    p.append(math.sqrt(90000+(x[i]-y[i])*(x[i]-y[i])))
	    if val == 200:
		Position_Set(List_Of_Turtles[i],val-275,200-x[i])
	    else:
		Position_Set(List_Of_Turtles[i],val,200-x[i])
	    if isGrant == 1:
		    List_Of_Turtles[i].right(180-math.degrees(angle)+90)
	    else:
		    List_Of_Turtles[i].right(math.degrees(angle)+90)
	    screen.update()
    
	for i in xrange(100):
		j=0
		for t in List_Of_Turtles:
			t.down()
			if (i*(i+1))/2 < p[j]:
				t.forward(i)
			j=j+1
		screen.update()
def Paint_Text(text,back,up):
	screen = turtle.getscreen()
	Temp_Turtle = turtle.Turtle()
	screen.tracer(0)
	Position_Set(Temp_Turtle,back,up)
	Temp_Turtle.write(text,font=("Comin Sans MS", 20, "normal"))
	Temp_Turtle.hideturtle()
	screen.update()


def Paint_VOQ(n,val):
	List_Of_Turtles = list()
	screen = turtle.getscreen()	
	screen.tracer(0)
	count = 0 
	for i in range(n):
		for j in range(n):
	  	  	List_Of_Turtles.append(turtle.Turtle())
			Position_Set(List_Of_Turtles[count],val+5,210-(10+90*i+j*10))
			if j in voqList[i]:
				List_Of_Turtles[count].begin_fill()
			for k in range(2):
				List_Of_Turtles[count].forward(7)
				List_Of_Turtles[count].left(90)
				List_Of_Turtles[count].forward(30)
				List_Of_Turtles[count].left(90)
			if j in voqList[i]:
				List_Of_Turtles[count].end_fill()
			List_Of_Turtles[count].hideturtle() 
			count += 1
	screen.update()

def Initialize_Draw(array,n,isGrant,val,sub_slot):
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
	
	if isGrant == 0 and sub_slot == 0:
		acceptCount = count+1
		for i in range(n):
			for j in range(n):
				acceptance[i][j]=0
				if(Packets_Matched[i][j] == 1):	#acceptance = [[0 for j in range(n)] for i in range(n)]
					x.append(10+i*90)
					y.append(10+j*90)
					count += 1
					Packets_Matched[i][j]=0
					voqList[i].remove(j)
		Paint_VOQ(n,600)	
	if isGrant == 1:
		Start_Draw(y,x,count,1,val,acceptCount)
	else:
		Start_Draw(x,y,count,isGrant,val,acceptCount)


def Paint_Circle(n,val):
	List_Of_Turtles = list()
	screen = turtle.getscreen()
	screen.tracer(0)
	for i in range(n):
	    	List_Of_Turtles.append(turtle.Turtle())
		Position_Set(List_Of_Turtles[i],val,200-(10+90*i))
		List_Of_Turtles[i].begin_fill()
		List_Of_Turtles[i].circle(15)
		List_Of_Turtles[i].end_fill()
		List_Of_Turtles[i].hideturtle() 
	for i in range(n):
	    	Temp_Turtle = turtle.Turtle()
		Position_Set(Temp_Turtle,val-300,200-(10+90*i))
		Temp_Turtle.begin_fill()
		Temp_Turtle.circle(15)
		Temp_Turtle.end_fill() 
		Temp_Turtle.hideturtle()
	screen.update()

def Position_Set(Temp_Turtle,back,up):
	Temp_Turtle.up()
	Temp_Turtle.back(back)
	Temp_Turtle.left(90)
	Temp_Turtle.forward(up)
	Temp_Turtle.down()

n = int(raw_input("Enter the number of port \n"))
Speed_Up_Factor = int(raw_input("Enter the speed up factor "))
acceptance = [[0 for j in range(n)] for i in range(n)]
Packets_Matched = [[0 for j in range(n)] for i in range(n)]
voqList = [[] for i in range(n)]
request = [[0 for j in range(n)] for i in range(n)]
accept = [[0 for j in range(n)] for i in range(n)]
temp_list = []
flag = 0
send_count = 0

for i in range(n):
	print "\n*********************Input Port", i,"************************"                           
        for j in range(n):
                temp = (randint(0,100) % 2)      ########## generating bernoulli traffic and keepng in request ###########
                if(temp == 1):
			print "#######################"
			print "PACKET"
			temp_rand = randint(1,5)
			#print temp_rand
			temp_rand = init_func( temp_rand, n )
			if(temp_rand == -1):
				print "Packed Dropped"
			else:
				request[i][int(temp_rand)] = temp
				voqList[i].append(int(temp_rand))
			        #voqList[i].append(j)

print request
temp = 0
iteration = 1
user_input = 1
time_slot = 4
no_of_itr = time_slot / Speed_Up_Factor
cycles = 0
sub_slot = 0

while(user_input == 1):
	print "*************ITERATION ",iteration,"*************"
	if sub_slot != no_of_itr:
		Paint_Text("REQUEST",550,225)
		Paint_VOQ(n,600)
	else:
		Paint_Text("REQUEST AND SENDING",550,225)
		sub_slot = 0
		for i in range(n):                           
			print "\n*********************Input Port", i,"************************"                           
        		for j in range(n):
                		temp = (randint(0,100) % 2)      ########## generating bernoulli traffic and keepng in request ###########
                		if(temp == 1):
					print "#######################"
					print "PACKET"
					temp_rand = randint(1,5)
					#print temp_rand
					temp_rand = init_func( temp_rand, n )
					if(temp_rand == -1):
						print "Packed Dropped"
					else:
						request[i][int(temp_rand)] = temp
						voqList[i].append(int(temp_rand))
			                        #voqList[i].append(j)
	Paint_Circle(n,550)
	for i in range(n):
		for j in range(n):
			if(request[i][j] == 1):
				print "voq",i+1,"sends request to output",j+1
		print "\n"
	print "-----------------------------------------"
	Initialize_Draw(request,n,0,550,sub_slot)	
	sub_slot += 1
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
	turtle.exitonclick()
	Paint_Text("GRANT",100,225)
	Paint_Circle(n,125)
	Paint_VOQ(n,175)
	Initialize_Draw(accept,n,1,-150,-1)
	turtle.exitonclick()
	
	Paint_Text("ACCEPT",-350,225)
	Paint_Circle(n,-300)
	Paint_VOQ(n,-250)
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
			Packets_Matched[i][temp_list[temp]] = 1
			send_count += 1
			flag = flag + 1
			for x in range(n):
				request[i][x] = 0
				request[x][temp_list[temp]] = 0
	        temp_list = []
	Initialize_Draw(acceptance,n,2,-300,-1)
	acceptance = [[0 for j in range(n)] for i in range(n)]
	if sub_slot == no_of_itr:	
		cycles += 1
	if(cycles == Speed_Up_Factor):
		cycles = 0
		user_input = int(raw_input("do you wanna continue\n"))
	#ppp = 0
	turtle.exitonclick()
