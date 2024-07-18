
from copy import deepcopy
from msvcrt import getch
import random
import cv2 as cv
import numpy as np
import threading
import time
from time import perf_counter

def reset():
	current_position = [0, 0]
	sn_pos_pts = [(0,0)]
	sn_len = 1
	return current_position, sn_pos_pts, sn_len
	

def move_and_render(limits,grid, px_per_segment, debug=False):
	# global direction, tar_pos, grid, px_per_segment,sn_pos_pts,WHITE,ORANGE,sn_len, running
	WHITE =(255,255,255)
	ORANGE = (0,160,255)
	
	min_x,max_x,min_y,max_y = limits
	
	running = True
	direction = "E"
	current_position = [0, 0]
	sn_pos_pts = [(0,0)]
	tar_pos = gentarget(limits)
	sn_len = 1
	target_fps = 5

	move_dict = {
		"N":moveUp,
		"S":moveDown,
		"E":moveRight,
		"W":moveLeft
	}
	#main game loop
	ts_last = perf_counter()
	while running:
		move_dict[direction](current_position,limits)
		if tar_pos == current_position:
			if debug:
				print(f'Target Found')
			while tar_pos == current_position or current_position in sn_pos_pts:
				tar_pos = gentarget(limits)
			if debug:
				print(f'new {tar_pos}')
			sn_len += 1
		sn_pos_pts, sn_len, current_position = enter_point(sn_pos_pts,\
													sn_len, current_position)

		if len(sn_pos_pts)>4:
			if current_position in sn_pos_pts[:-1]:
				reset()
				print("reset")

		img = grid.copy()
		# renderpoint(current_position,px_per_segment,img,ORANGE)
		img = renderpoints(sn_pos_pts,px_per_segment,img,ORANGE)
		renderpoint(tar_pos,px_per_segment,img,WHITE)
		cv.imshow('Snake Game - Press Q to exit',img)
		cv.namedWindow('Snake Game - Press Q to exit',cv.WINDOW_NORMAL)
		cv.waitKey(1)
		t_delay = (0.4*10/(10+sn_len))
		time.sleep(t_delay)

def listen_and_direct():
	# global direction, running
	while True:
	# print(f'Distance from zero: , {current_position}')
		key = ord(getch())
		print(key), time.sleep(1)
		if key == 27: #ESC
			running = 1
			break
		elif key == 13: #Enter
			print('selected')
		elif key == 32: #Space
			print('jump')
		elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
			key = ord(getch())
			if key == 80: #Down arrow
				print('down')
				# moveDown()
				if direction =="N":
					pass
				else:
					direction = "S"
			elif key == 72: #Up arrow
				print('up')
				# moveUp()
				if direction =="S":
					pass 
				else:
					direction = "N"
			elif key == 75: #Left arrow
				print('left')
				# moveLeft()
				if direction =="E":
					pass
				else:
					direction = "W"
			elif key == 77: #Right arrow
				print('right')
				# moveRight()
				if direction =="W":
					pass
				else:
					direction = "E"
		# time.sleep(0.1)

def enter_point(sn_pos_pts,sn_len, current_position, debug=False):
	# global current_position, sn_len, sn_pos_pts
	if len(sn_pos_pts) == sn_len:
		b = [deepcopy(current_position[0]),deepcopy(current_position[1])]
		sn_pos_pts.pop(0)
		if debug:
			print(b)
		sn_pos_pts.append(b)

	elif len(sn_pos_pts) < sn_len:
		b = [deepcopy(current_position[0]),deepcopy(current_position[1])]
		sn_pos_pts.append(b)
	
	else:
		pass
	if debug:
		print(sn_pos_pts)

	return sn_pos_pts, sn_len, current_position

def rendergrid(max_x,max_y,px_per_segment):
	x = int((1+max_x)*px_per_segment)
	y = int((1+max_y)*px_per_segment)
	grid = np.zeros((y,x,3), np.uint8)
	return grid

def renderpoints(list,px_per_segment,grid,color):
	for current_position in list:
		img = grid
		x = int(px_per_segment*current_position[1])
		y = int(px_per_segment*current_position[0])
		intpos = (y,x)
		x2 = x + px_per_segment
		y2 = y + px_per_segment

		finpos = (y2,x2)
		img = cv.rectangle(img,(intpos),(finpos),color,-1)
	return img

def renderpoint(current_position,px_per_segment,grid,color):
	x = int(px_per_segment*current_position[1])
	y = int(px_per_segment*current_position[0])
	intpos = (y,x)
	x2 = x + px_per_segment
	y2 = y + px_per_segment

	finpos = (y2,x2)
	cv.rectangle(grid,(intpos),(finpos),color,-1)

def gentarget(limits, existing_positions=None):
	#add a check against current positions
	min_x,max_x,min_y,max_y = limits
	while True:
		x = random.randint(min_x, max_x)
		y = random.randint(min_y, max_y)
		new_tar = [x,y]
		if existing_positions is None:
			break
		elif new_tar in existing_positions:
			pass
		else:
			break

	return new_tar

def moveRight(current_position,limits):
	# global current_position,direction, sn_len,sn_pos_pts
	min_x,max_x,min_y,max_y = limits
	if current_position[0] == max_x:
		return None
	else:
		current_position[0] += 1
		direction = 'E'
		return direction, current_position

def moveLeft(current_position, min_x):
	# global current_position,direction,sn_len,sn_pos_pts
	if current_position[0] == min_x:
		return None
	else:
		current_position[0] -= 1
		direction = 'W'
		return direction, current_position

def moveUp(current_position, min_y):
	# global current_position,direction,sn_len,sn_pos_pts
	if current_position[1] == min_y:
		return None
	else:
		current_position[1] -= 1
		direction = 'N'
		return direction, current_position

def moveDown(current_position, max_y):
	# global current_position,direction,sn_len,sn_pos_pts
	if current_position[1] == max_y:
		return None
	else:
		current_position[1] += 1
		direction = 'S'
		return direction, current_position

# def print_direction():
# 	global direction
# 	while True:
# 		print(direction)
# 		time.sleep(1)


def main():
	direction = "E"
	current_position = [0,0]
	tar_pos = [0,0]
	min_x = 0
	min_y = 0
	max_x = 30
	max_y = 30
	px_per_segment = 25
	sn_len = 1
	sn_pos_pts = [(0,0)]
	running = 0

	limits = [min_x,max_x,min_y,max_y]

	# tar_pos = gentarget(limits)
	grid = rendergrid(max_x,max_y,px_per_segment)
	move_and_render(limits, grid, px_per_segment)
	print("reacherd")
	# t1 = threading.Thread(target=listen_and_direct, args=()) 
	# t2 = threading.Thread(target=move_and_render, args=()) 
	# t1.start()
	# t2.start()
	

if __name__ == '__main__':
# Create two threads as follows
	main()
