
from copy import deepcopy
from msvcrt import getch
import random
import cv2 as cv
import numpy as np
# import threading
import time
from time import perf_counter
import keyboard
import sys

class GameStatus:
	def __init__(self):
		self.is_running = True
		self.direction = "E"
	
	def __repr__(self):
		return self.is_running

def reset():
	current_position = [0, 0]
	sn_pos_pts = [(0,0)]
	sn_len = 1
	return current_position, sn_pos_pts, sn_len	

def move_and_render(limits,grid, px_per_segment, debug=False):
	# global direction
	WHITE =(255,255,255)
	ORANGE = (0,160,255)
	WINDOW_NAME = 'Snake Game - Press Q to exit'
	
	# min_x,max_x,min_y,max_y = limits
	
	game_status = GameStatus()

	running = True

	current_position = [0, 0]
	sn_pos_pts = [(0,0)]
	tar_pos = gentarget(limits)
	sn_len = 1
	img = grid.copy()
	# target_fps = 5

	move_dict = {
		"N":moveUp,
		"S":moveDown,
		"E":moveRight,
		"W":moveLeft
	}

	keyboard.add_hotkey("up",		lambda: detect_keypress("N", game_status))
	keyboard.add_hotkey("down",		lambda: detect_keypress("S", game_status))
	keyboard.add_hotkey("left",		lambda: detect_keypress("W", game_status))
	keyboard.add_hotkey("right",	lambda: detect_keypress("E", game_status))
	keyboard.add_hotkey("shift+q",	lambda: detect_keypress("Q", game_status, debug=True))
	
	#main game loop
	ts_last = perf_counter()
	while game_status.is_running:
		direction = game_status.direction
		ts_current = perf_counter()
		t_delay = (0.4*10/(10+sn_len))
		
		#only move and render when timer trips 
		if ts_current - ts_last > t_delay:
			if move_dict[direction](current_position,limits) is None:
				#detect wall collisions and reset
				current_position, sn_pos_pts, sn_len = reset()
				game_status.direction = "E"
				tar_pos = gentarget(limits)
			#detect target collisions
			if tar_pos == current_position:
				if debug:
					print(f'Target Found')
				while tar_pos == current_position or current_position in sn_pos_pts:
					tar_pos = gentarget(limits,sn_pos_pts)
				if debug:
					print(f'new {tar_pos}')
				sn_len += 1
			sn_pos_pts, sn_len, current_position = enter_point(sn_pos_pts,\
														sn_len, current_position)
			#detect self collisions
			if len(sn_pos_pts)>4:
				if current_position in sn_pos_pts[:-1]:
					current_position, sn_pos_pts, sn_len = reset()
					print("reset")
			
			#render image and display
			# t_delay = (0.4*10/(10+sn_len))
		
		#update img only on following step
		if ts_current - ts_last >= t_delay:
			img = grid.copy()
			img = renderpoints(sn_pos_pts,px_per_segment,img,ORANGE)
			renderpoint(tar_pos,px_per_segment,img,WHITE)
			ts_last = ts_current

		cv.imshow(WINDOW_NAME,img)
		cv.namedWindow(WINDOW_NAME,cv.WINDOW_NORMAL)
		cv.waitKey(1)

		# t_delay = (0.4*10/(10+sn_len))
		# time.sleep(t_delay)

def valid_direction_change(current_drx, desired_drx):
	# prevent doubling back
	ignored_direction_changes = {
		"N":["N", "S"],
		"S":["N", "S"],
		"E":["E", "W"],
		"W":["E", "W"]}
	if desired_drx not in ignored_direction_changes[current_drx]:
		return True
	else: 
		return False

def detect_keypress(direction_in, game_status,  debug=False):
	
	if direction_in == "Q": 
		game_status.is_running = False 
	elif valid_direction_change(game_status.direction, direction_in):
		game_status.direction = direction_in
	else:
		pass
	if debug:
		print("Direction Press: ",direction_in)

def enter_point(sn_pos_pts,sn_len, current_position, debug=False):
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
	min_x,max_x,min_y,max_y = limits
	if current_position[0] == max_x:
		return None
	else:
		current_position[0] += 1
		direction = 'E'
		return direction, current_position

def moveLeft(current_position, limits):
	min_x,max_x,min_y,max_y = limits
	if current_position[0] == min_x:
		return None
	else:
		current_position[0] -= 1
		direction = 'W'
		return direction, current_position

def moveUp(current_position, limits):
	min_x,max_x,min_y,max_y = limits
	if current_position[1] == min_y:
		return None
	else:
		current_position[1] -= 1
		direction = 'N'
		return direction, current_position

def moveDown(current_position, limits):
	min_x,max_x,min_y,max_y = limits
	if current_position[1] == max_y:
		return None
	else:
		current_position[1] += 1
		direction = 'S'
		return direction, current_position

def main():

	min_x = 0
	min_y = 0
	max_x = 10
	max_y = 10
	px_per_segment = 25

	limits = [min_x,max_x,min_y,max_y]
	grid = rendergrid(max_x,max_y,px_per_segment)
	move_and_render(limits, grid, px_per_segment)

if __name__ == '__main__':
	main()
