import numpy as np
# import pygame
import matplotlib.pyplot as plt

SIZE = WIDTH, HEIGHT = np.array([800,600])#screen window
x_spawn = [i for i in range(-50,-10)] + [i for i in range(WIDTH+10, WIDTH+50)]#spawn outside the window
y_spawn = [i for i in range(-50,-10)] + [i for i in range(HEIGHT+10, HEIGHT+50)]#spawn outside the window


class Boid(object):
	"""Boid Object"""
	def __init__(self,c='g', position=0): #initialize position and velocity
		if not position:
			self.position = np.array([np.random.choice(x_spawn), np.random.choice(y_spawn)])
		else:
			self.position = np.array(position)
		self.velocity = np.array([0,0])
		self.color = c

	def __sub__(self, other):
		return (self.position - other.position)

	def __str__(self):
		return (f'{self.position}')


def COH_RULE(all_boids, boid, COH_per=1):
	'''Coherence rule to make boids to move to a general centre of mass of the flock'''
	avg_vector = 0
	for each in all_boids:
		if not (each is boid):
			avg_vector = avg_vector + each.position
	try:
		vector = np.array(avg_vector/(len(all_boids)-1)) - boid.position
		return (vector * COH_per / 100)
	
	except:
		return 0
	
def VEL_RULE(all_boids, boid, FOV=100, ALI_per= 0.05):
	'''Velocity rule to have the boid match the general velocity'''
	avg_vector = 0
	for each in all_boids:
		if not (each is boid):
			if np.around(np.linalg.norm(each-boid),2) < FOV:
				avg_vector = avg_vector + each.velocity
	try:
		vector = np.array(avg_vector/(len(all_boids)-1)) - boid.position
		return (vector * ALI_per / 100)

	except:
		print('triggred')
		return 0

def SEP_RULE(all_boids, boid, FOV=100, SEP_per=100):
	'''Seperation rule to not have a boid colide with other'''
	vector = 0
	for each in all_boids:
		if not (each is boid):
			if np.around(np.linalg.norm(each-boid),2) < FOV:
				vector = vector - (each - boid)
	return (vector * SEP_per / 100)

def BOUND_RULE(boid, FOV=100, factor=50):
	'''Keep boids from moving off the screen'''
	padding = 0
	xdist = 0
	ydist = 0
	if boid.position[0] + FOV > WIDTH - padding:
		xdist = -factor
	elif boid.position[0] - FOV < 0 + padding:
		xdist = factor
	if boid.position[1] + FOV > HEIGHT - padding:
		ydist = -factor
	elif boid.position[1] - FOV < 0 + padding:
		ydist = factor
	return np.array([xdist, ydist])

def Tend_centre(boid, percent=1):
	goal_pos = SIZE/2
	return (goal_pos - boid.position) * percent / 100

def limit_speed(boid, v_lim=20): 
	vel = np.linalg.norm(boid.velocity)
	# print(vel)
	if vel > v_lim:
		# print(vel)
		boid.velocity = ((boid.velocity / vel)*v_lim)

def rule_Handler(all_boids):
	'''handler for moving all boids, each frame is equvalent to calling this function once'''
	for boid in all_boids:
		plt.scatter(boid.position[0],boid.position[1], marker='o')
	for boid in all_boids:
		v1 = COH_RULE(all_boids, boid)
		# print(f'COM: {v1}')
		v2 = VEL_RULE(all_boids, boid)
		# print(f'velocity: {v2}')
		v3 = SEP_RULE(all_boids, boid)
		# print(f'sep: {v3}')
		v4 = BOUND_RULE(boid)
		# print(f'boundry: {v4}')
		v5 = Tend_centre(boid)
		# print(f'centre: {v5}')
		v1 = v1 * 1
		v2 = v2 * 1
		v3 = v3 * 1
		v4 = v4 * 1
		v5 = v5 * 1
		boid.velocity = boid.velocity + v1 + v2 + v3 + v4 + v5
		limit_speed(boid)
		np.around(boid.velocity, 2, boid.velocity)
		boid.position = boid.position + boid.velocity
		np.around(boid.position, 2, boid.position)
		
		# print(boid.velocity, boid.position)

def initialize_pos(n=10): #initializing boids
	# All_boids = [Boid('r'), Boid('b'), Boid('g'), Boid('c')]
	All_boids = [Boid() for _ in range(n)]
	return All_boids

def main():
	all_boids = initialize_pos(20)
	# for i in all_boids:
	# 	print(i)
	for frame in range(100):
		rule_Handler(all_boids)
		if frame > 15:
			for i in all_boids:
				if np.any(i.position > SIZE) or np.any(i.position < [0,0]):
					print("outside")
		# for i in all_boids:
		# 	print(i)	
	# for i in all_boids:
		# print(i)
		
main()
plt.show()


# k = Boid()
# m = Boid()

# print(k,m)
# print(np.around(np.linalg.norm(k-m),2))

