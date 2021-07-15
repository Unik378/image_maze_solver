import numpy as np;
from PIL import Image;
import argparse
from gifgenerator import *
import os
import glob

def argParser():
	parser = argparse.ArgumentParser()

	parser.add_argument('--image', nargs='?', default='maze.png', help="Path to maze image")

	# parser.add_argument('--output', nargs='?', default='', help="File to save Embeedings of combined input graph")

	parser.add_argument('--startx', type=int, default=0,help='Start x of maze')
	parser.add_argument('--starty', type=int, default=0,help='Start y of maze')
	parser.add_argument('--endx', type=int, default=0,help='End x of maze')
	parser.add_argument('--endy', type=int, default=0,help='End y of maze')

	return parser.parse_args()

class Maze:

	def __init__(self, imagePath, start=(0,0), end=(0,0)):
		self.imagePath = imagePath
		self.image = Image.open(imagePath)
		self.image = self.image.convert('RGB')
		self.pixels = self.image.load()

		self.GREEN = (0,255,0)
		self.RED = (255,0,0)
		self.WHITE = (255,255,255)
		self.BLACK = (0,0,0)

		self.start = start
		self.end = end

		self.frequency = int(self.image.size[0]*self.image.size[1]/50)
		self.frameCount = 0

	def closestColor(self,color):
		val = 0.299*color[0] + 0.587*color[1] + 0.114*color[2]
		if(val > 200):
			return self.WHITE
		else:
			return self.BLACK

	def cleanImage(self):
		x,y = self.image.size
		for i in range(x):
			for j in range(y):
				self.pixels[i,j] = self.closestColor(self.pixels[i,j])

	def showImage(self):
		self.image.show()

	def fixWalls(self):
		x,y = self.image.size

		for i in range(x-1):
			for j in range(y-1):
				currPix = (i,j)
				nextPix = (i,j+1)
				belowPix = (i+1,j)
				diagonalPix = (i+1,j+1)

				if (self.pixels[currPix] == self.WHITE and self.pixels[diagonalPix] == self.WHITE and self.pixels[nextPix] == self.BLACK and self.pixels[belowPix] == self.BLACK) or (self.pixels[currPix] == self.BLACK and self.pixels[diagonalPix] == self.BLACK and self.pixels[nextPix] == self.WHITE and self.pixels[belowPix] == self.WHITE):
					self.pixels[currPix] = self.BLACK
					self.pixels[nextPix] = self.BLACK
					self.pixels[diagonalPix] = self.BLACK
					self.pixels[belowPix] = self.BLACK

	def isValid(self,vertex):
		x,y = self.image.size
		if vertex[0] >= 0 and vertex[0] < x and vertex[1] >= 0 and vertex[1] < y:
			return True

		return False

	def getNeighbours(self,vertex):
		x = vertex[0]
		y = vertex[1]
		return [(x-1,y-1),(x-1,y+1),(x+1,y+1),(x+1,y-1),(x-1,y),(x,y+1),(x+1,y),(x,y-1)]

	def display(self,parent):
		for i in parent:
			# for j in i;
			print(i)
			
		print("\n\n")

	def bfs(self):
		q = []
		x,y = self.image.size
		parent = []
		for i in range(x):
			temp = []
			for j in range(y):
				temp.append((-1,-1))
			parent.append(temp)


		image = self.image.copy()
		q.append(self.start)
		pixels = image.load()
		pixels[self.start] = self.GREEN
		iterations = 0

		while q:
			vertex = q.pop(0)

			if vertex == self.end:
				print("found")
				i = self.end[0]
				j = self.end[1]
				path = []

				while parent[i][j] != (-1,-1):
					path.append((i,j))
					i,j = parent[i][j]
				path.append((i,j))
				return path

			neighbours = self.getNeighbours(vertex)
			for neighbour in neighbours:
				if self.isValid(neighbour) and pixels[neighbour] == self.WHITE:
					pixels[neighbour] = self.GREEN
					parent[neighbour[0]][neighbour[1]] = vertex
					q.append(neighbour)

			if iterations%self.frequency == 0:
				image.save('./frames/'+str(self.frameCount)+'.jpg')
				self.frameCount = self.frameCount + 1
			
			iterations = iterations+1
		return []

	def solve(self):
		self.cleanImage()
		self.fixWalls()

		print(self.frequency)

		path = self.bfs()
		if path:
			for pos in path:
				self.pixels[pos] = self.GREEN
				for neighbour in self.getNeighbours(pos):
					if self.isValid(neighbour) and self.pixels[neighbour] == self.WHITE:
						self.pixels[neighbour] = self.GREEN
			
			self.showImage()
			self.image.save('./output/output.jpg')
			createGIF(self.imagePath, self.frameCount)

		else:
			print("Path not found")

def main(arg):
	url = arg.image
	start = (arg.startx,arg.starty)
	end = (arg.endx,arg.endy)
	maze = Maze(url,start,end)
	files = glob.glob('./frames/*')
	for f in files:
		os.remove(f)
	maze.solve()

if __name__ == '__main__':
	arg = argParser()
	main(arg)