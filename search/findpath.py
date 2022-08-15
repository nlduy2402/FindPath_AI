import pygame
import math
from queue import PriorityQueue
import queue
SIZE = 600
SCREEN = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Search Algorithm")

EXPANDED = (255, 128, 0)
OPENED = (0, 255, 0)
START_END = (0, 0, 255)
OBSTACLE = (255, 150, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PATH = (255, 50, 20)
ORANGE = (255, 165 ,0)
BLACK = (128, 128, 128)
BORDER=(81,81,81)



class Square:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == EXPANDED

	def is_open(self):
		return self.color == OPENED

	def is_Obstacle(self):
		return self.color == OBSTACLE or self.color == BORDER

	def is_start(self):
		return self.color == START_END

	def is_end(self):
		return self.color == START_END

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = START_END

	def make_Expanded(self):
		self.color = EXPANDED

	def make_open(self):
		self.color = OPENED

	def make_Obstacle(self):
		self.color = OBSTACLE

	def make_end(self):
		self.color = START_END

	def make_path(self):
		self.color = PATH
	
	def create_border(self):
		self.color = BORDER

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

	def Get_neighbor(self, Graph):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not Graph[self.row + 1][self.col].is_Obstacle(): # DOWN
			self.neighbors.append(Graph[self.row + 1][self.col])

		if self.row > 0 and not Graph[self.row - 1][self.col].is_Obstacle(): # UP
			self.neighbors.append(Graph[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not Graph[self.row][self.col + 1].is_Obstacle(): # RIGHT
			self.neighbors.append(Graph[self.row][self.col + 1])

		if self.col > 0 and not Graph[self.row][self.col - 1].is_Obstacle(): # LEFT
			self.neighbors.append(Graph[self.row][self.col - 1])

	def __lt__(self, other):
		return False

# heuristic
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

#backtracking path
def Path_finding(path, current, draw):
	a=0
	while current in path:
		a+=1
		current = path[current]
		current.make_path()
		draw()
	print("path cost:"+str(a))

# A*
def Astar(draw, Graph, start, end):
	count = 0
	Q = PriorityQueue()
	Q.put((0, count, start))
	path = {}
	cost = {square: float("inf") for row in Graph for square in row}
	cost[start] = 0
	f = {square: float("inf") for row in Graph for square in row}
	f[start] = h(start.get_pos(), end.get_pos())

	open_list = {start}

	while not Q.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = Q.get()[2]
		open_list.remove(current)

		if current == end:
			Path_finding(path, end, draw)
			end.make_end()
			print("expanded node:"+str(count-len(open_list)))
			return True

		for neighbor in current.neighbors:
			temp_cost = cost[current] + 1

			if temp_cost < cost[neighbor]:
				path[neighbor] = current
				cost[neighbor] = temp_cost
				f[neighbor] = temp_cost + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_list:
					count += 1
					Q.put((f[neighbor], count, neighbor))
					open_list.add(neighbor)
					neighbor.make_open()
		draw()
		if current != start:
			current.make_Expanded()
	print("None path")
	print("expanded node:"+str(count-len(open_list)))
	return False

# UCS
def UCS(draw, Graph, start, end):
	count = 0
	Q = PriorityQueue()
	Q.put((0, count, start))
	path = {}
	cost = {spot: float("inf") for row in Graph for spot in row}
	cost[start] = 0

	open_list = {start}

	while not Q.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = Q.get()[2]
		open_list.remove(current)

		if current == end:
			Path_finding(path, end, draw)
			end.make_end()
			print("expanded node:"+str(count-len(open_list)))
			return True

		for neighbor in current.neighbors:
			temp_cost = cost[current] + 1
			if temp_cost < cost[neighbor]:
				path[neighbor] = current
				cost[neighbor] = temp_cost
				if neighbor not in open_list:
					count += 1
					Q.put((cost[neighbor], count, neighbor))
					open_list.add(neighbor)
					neighbor.make_open()
		draw()
		if current != start:
			current.make_Expanded()
	print("None path")
	print("expanded node:"+str(count-len(open_list)))
	return False

# BFS
def BFS(draw, Graph, start, end):
	count = 0
	Q = queue.Queue()
	Q.put((count, start))
	path = {}
	# cost = {spot: float("inf") for row in grid for spot in row}
	# cost[start] = 0
	# f = {spot: float("inf") for row in grid for spot in row}
	# f[start] = h(start.get_pos(), end.get_pos())
	open_list = {start}
	while not Q.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = Q.get()[1]
		open_list.remove(current)

		if current == end:
			Path_finding(path, end, draw)
			end.make_end()
			print("expanded node:"+str(count-len(open_list))) # số node expanded
			return True

		for neighbor in current.neighbors:
			if(path.get(neighbor,None) == None and neighbor != start):
				path[neighbor] = current
				if neighbor not in open_list:
					count += 1
					Q.put((count, neighbor))
					open_list.add(neighbor)
					neighbor.make_open()

		draw()
		if current != start:
			current.make_Expanded()
	print("None path")
	print("expanded node:"+str(count-len(open_list)))
	return False

# GBFS
def GBFS(draw, Graph, start, end):
	count = 0
	Q = PriorityQueue()
	Q.put((0, count, start))
	path = {}
	open_list = {start}

	while not Q.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = Q.get()[2]
		open_list.remove(current)
		min_heu=999
		if current == end:
			Path_finding(path, end, draw)
			end.make_end()
			print("expanded node:"+str(count-len(open_list)))
			return True
		
		for neighbor in current.neighbors:
			if(path.get(neighbor,None) == None and neighbor != start):
				path[neighbor] = current
				if neighbor not in open_list:
					count += 1
					Q.put((h(neighbor.get_pos(),end.get_pos()), count,neighbor))
					open_list.add(neighbor)
					neighbor.make_open()
			
		draw()

		if current != start:
			current.make_Expanded()
	print("None path")
	print("expanded node:"+str(count-len(open_list)))
	return False

# initialize matrix
def CreateGraph(rows, width):
	G = []
	size = width // rows
	for i in range(rows):
		G.append([])
		for j in range(rows):
			sqr = Square(i, j, size, rows)
			G[i].append(sqr)
	return G

# draw line
def Draw_Line(screen, rows, width):
	size = width // rows
	for i in range(rows):
		pygame.draw.line(screen, BLACK, (0, i * size), (width, i * size))
		for j in range(rows):
			pygame.draw.line(screen, BLACK, (j * size, 0), (j * size, width))

# Draw matrix
def Draw(screen, Graph, rows, width):
	screen.fill(WHITE)

	for row in Graph:
		for square in row:
			if(square.row == 0 or square.row==22):
				if(square.col <= 18):
					square.create_border()
			if(square.col == 0 or square.col == 18):
				if(square.row <= 22):
					square.create_border()
			square.draw(screen)

	Draw_Line(screen, rows, width)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	size = width // rows
	y, x = pos
	row = y // size
	col = x // size
	return row, col

# Draw obstacle
def DrawObstacle(screen, Graph, rows, width,list_obs):
	for row in Graph:
		for square in row:
			if(square.get_pos() in list_obs and not square.is_Obstacle()):
				square.make_Obstacle()
			square.draw(screen)

	Draw_Line(screen, rows, width)
	pygame.display.update()

# -- MAIN --
def main(screen, width):
	ROWS = 25
	G = CreateGraph(ROWS, width)
	run = True
	src=None
	des=None
	start = None
	end = None	
	size=[]
	obstacle=[]	

	# Get Data from input.txt
	with open("input.txt","r") as fobj:
		line=fobj.readlines()
		for i in range(len(line)):
			line[i]=line[i].split()
			line[i]=list(map(int,line[i]))
		size = line[0]
		src=(line[1][0],line[1][1])
		des=(line[1][2],line[1][3])
		for i in range(3,len(line)):
			obstacle.append(line[i])

	list_obs=[]
	for i in range(len(obstacle)):
		obs=[]
		for j in range(0,len(obstacle[i])-1,2):
			tup_obs = (obstacle[i][j],size[1]-obstacle[i][j+1])
			obs.append(tup_obs)
		list_obs.append(obs)
	
	# add obstacle
	lobs1=[(4,13),(4,12),(4,11),(4,10),
		(6,9),(7,8),(5,14),(6,14),(7,14),
		(8,14),(9,12),(9,11),(9,10),(9,9)]
	lobs2=[(8,5),(8,4),(8,3),(8,2),(9,6),(10,6),
	(11,6),(12,6),(9,2),(10,3),(11,4),(12,5)]
	lobs3=[(11,16),(11,15),(11,14),(11,13),(12,12),
	(13,12),(12,17),(13,17),(14,16),(14,15),(14,13),(14,14)]
	list_obs.append(lobs1)
	list_obs.append(lobs2)
	list_obs.append(lobs3)
	while run:
		Draw(screen, G, ROWS, width)
		for i in range(len(list_obs)):
			DrawObstacle(screen,G,ROWS,width,list_obs[i])

		pygame.display.update()
		# initialize start, end
		squareStart=G[src[0]][size[1]-src[1]]
		start=squareStart
		start.make_start()
		squareEnd=G[des[0]][size[1]-des[1]]
		end=squareEnd
		end.make_end()	
	
		for event in pygame.event.get():
			# 
			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				square = G[row][col]
				if square != end and square != start:
					square.make_Obstacle()
			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				square = G[row][col]
				square.reset()
				if square == start:
					start = None
				elif square == end:
					end = None

			if event.type == pygame.QUIT:
				run = False
			# R:reset		1:BFS		2:UCS		3:GBFS		4:A*
			if event.type == pygame.KEYDOWN:
				for row in G:
						for square in row:
							square.Get_neighbor(G)
				if event.key == pygame.K_1:
					BFS(lambda: Draw(screen, G, ROWS, width), G, start, end)
				if event.key == pygame.K_2:
					UCS(lambda: Draw(screen, G, ROWS, width), G, start, end) 
				if event.key == pygame.K_3:
					GBFS(lambda: Draw(screen, G, ROWS, width), G, start, end) 
				if event.key == pygame.K_4:
					Astar(lambda: Draw(screen, G, ROWS, width), G, start, end) 
				if event.key == pygame.K_r:
					start = None
					end = None
					G = CreateGraph(ROWS, width)

		pygame.display.update()

	pygame.quit()

main(SCREEN, SIZE)