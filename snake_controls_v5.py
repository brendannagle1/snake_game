
from copy import deepcopy
from msvcrt import getch
import random
import cv2 as cv
import numpy as np
import threading
import time

direction = "E"
pos = [0,0]
tar_pos = [0,0]
min_x = 0
min_y = 0
max_x = 30
max_y = 30
dim_mult = 25
sn_len = 1
sn_pos_pts = [(0,0)]
end = 0

white =(255,255,255)
orange = (0,160,255)

def reset():
	global pos, sn_pos_pts, sn_len
	pos = [0, 0]
	sn_pos_pts = [(0,0)]
	sn_len = 1

def move_and_render():
	global direction, tar_pos, grid, dim_mult,sn_pos_pts,white,orange,sn_len, end
	while True:
		if end == 1:
			break

		if direction == "N":
			fup()
		elif direction == "S":
			fdown()
		elif direction =="E":
			fright()
		elif direction =="W":
			fleft()

		if tar_pos == pos:
			print(f'Target Found')
			while tar_pos == pos or pos in sn_pos_pts:
				tar_pos = gentarget(min_x,max_x,min_y,max_y)
			print(f'new {tar_pos}')
			sn_len += 1
		enter_point()

		if len(sn_pos_pts)>4:
			if pos in sn_pos_pts[:-1]:
				reset()
				print("reset")

		img = grid.copy()
		# renderpoint(pos,dim_mult,img,orange)
		img = renderpoints(sn_pos_pts,dim_mult,img,orange)
		renderpoint(tar_pos,dim_mult,img,white)
		cv.imshow('image',img)
		cv.namedWindow('image',cv.WINDOW_NORMAL)
		cv.waitKey(1)
		t_delay = (0.4*10/(10+sn_len))
		time.sleep(t_delay)

def listen_and_direct():
	global direction, end
	while True:
	# print(f'Distance from zero: , {pos}')
		key = ord(getch())
		if key == 27: #ESC
			end = 1
			break
		elif key == 13: #Enter
			print('selected')
		elif key == 32: #Space
			print('jump')
		elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
			key = ord(getch())
			if key == 80: #Down arrow
				print('down')
				# fdown()
				if direction =="N":
					pass
				else:
					direction = "S"
			elif key == 72: #Up arrow
				print('up')
				# fup()
				if direction =="S":
					pass 
				else:
					direction = "N"
			elif key == 75: #Left arrow
				print('left')
				# fleft()
				if direction =="E":
					pass
				else:
					direction = "W"
			elif key == 77: #Right arrow
				print('right')
				# fright()
				if direction =="W":
					pass
				else:
					direction = "E"
		# time.sleep(0.1)

def enter_point():
	global pos, sn_len, sn_pos_pts
	if len(sn_pos_pts) == sn_len:
		b = [deepcopy(pos[0]),deepcopy(pos[1])]
		sn_pos_pts.pop(0)
		print(b)
		sn_pos_pts.append(b)

	elif len(sn_pos_pts) < sn_len:
		b = [deepcopy(pos[0]),deepcopy(pos[1])]
		sn_pos_pts.append(b)
	
	else:
		pass
	print (sn_pos_pts)

def rendergrid(maxx,maxy,mult):
	x = int((1+maxx)*mult)
	y = int((1+maxy)*mult)
	grid = np.zeros((y,x,3), np.uint8)
	return grid

def renderpoints(list,mult,grid,color):
	for pos in list:
		img = grid
		x = int(mult*pos[1])
		y = int(mult*pos[0])
		intpos = (y,x)
		x2 = x + mult
		y2 = y + mult

		finpos = (y2,x2)
		img = cv.rectangle(img,(intpos),(finpos),color,-1)
	return img

def renderpoint(pos,mult,grid,color):
	x = int(mult*pos[1])
	y = int(mult*pos[0])
	intpos = (y,x)
	x2 = x + mult
	y2 = y + mult

	finpos = (y2,x2)
	cv.rectangle(grid,(intpos),(finpos),color,-1)

def gentarget(minx,maxx,miny,maxy):
	x = random.randint(minx, maxx)
	y = random.randint(miny, maxy)
	new_tar = [x,y]
	return new_tar

def fright():
	global pos,direction, sn_len,sn_pos_pts
	
	if pos[0] == max_x:
		reset()
	else:
		pos[0] += 1
		direction = 'E'

def fleft():
	global pos,direction,sn_len,sn_pos_pts
	if pos[0] == min_x:
		reset()
	else:
		pos[0] -= 1
		direction = 'W'

def fup():
	global pos,direction,sn_len,sn_pos_pts
	if pos[1] == min_y:
		reset()
	else:
		pos[1] -= 1
		direction = 'N'

def fdown():
	global pos,direction,sn_len,sn_pos_pts
	if pos[1] == max_y:
		reset()
	else:
		pos[1] += 1
		direction = 'S'

def print_direction():
	global direction
	while True:
		print(direction)
		time.sleep(1)

tar_pos = gentarget(min_x,max_x,min_y,max_y)

grid = rendergrid(max_x,max_y,dim_mult)

if __name__ == '__main__':

# Create two threads as follows
	t1 = threading.Thread(target=listen_and_direct, args=()) 
	t2 = threading.Thread(target=move_and_render, args=()) 
	t1.start()
	t2.start()
	