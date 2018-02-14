#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from tkinter import *
import random

class GraphShow:

	def __init__(self, graph, width = 800, height = 600):
		self.window = Tk()
		self.graph = NodePosition(graph, width, height)
		self.width = width
		self.height = height
		self.canvas = Canvas(self.window, width = self.width, height = self.height, background = "white")
		self.canvas.pack()
		self.draw_graph()

	def loop(self):
		self.window.mainloop()

	def create_round(self, x, y, r, color):
		rd2 = r / 2
		x1 = x - rd2
		y1 = y - rd2
		x2 = x + rd2
		y2 = y + rd2
		self.canvas.create_oval(x1, y1, x2, y2, fill = color)

	def create_node(self, node):
		self.create_round(node["x"], node["y"], 20, node["color"])
		self.canvas.create_text(node["x"], node["y"], text = node["name"])

	def create_link(self, node1, node2):
		self.canvas.create_line(node1["x"], node1["y"], node2["x"], node2["y"], arrow='first', arrowshape=(20, 25, 5))

	def draw_graph(self):
		links = self.graph.getLinks()
		for link in links:
			self.create_link(link[0], link[1])
		nodes = self.graph.getNodes()
		for node in nodes:
			self.create_node(node)

class NodePosition:

	def __init__(self, graph, width, height):
		self.width = width
		self.height = height
		self.graph = graph
		self.nodes = []
		self.links = []
		self.initNodes()
		self.initLinks()
		# self.posNodesRand()
		size = self.posNodesI()
		self.posGrid(size)

	def initNodes(self):
		for i, node in enumerate(self.graph["idict"]):
			name = node[:1]
			color = "white"
			if self.graph["list"][i] == 1:
				color = "green"
			elif self.graph["list"][i] == 2:
				color = "blue"
			self.nodes.append({"x" : 0, "y": 0, "name": name, "id": node, "color": color})

	def initLinks(self):
		for i, line in enumerate(self.graph["matrix"]):
			for j, node in enumerate(line):
				if node == 1:
					self.links.append([i, j])

	def posNodesRand(self):
		history = []
		marge = 50
		grid = 10
		w = (self.width - marge * 2) / grid
		h = (self.height - marge * 2) / grid
		for node in self.nodes:
			exist = True
			x = 0
			y = 0
			while exist:
				exist = False
				x = int(random.random() * grid)
				y = int(random.random() * grid)
				for hl in history:
					if hl[0] == x and hl[1] == y:
						exist = True
			history.append([x, y])
			node["x"] = marge + x * w
			node["y"] = marge + y * h

	def posGrid(self, grid = 20, marge = 20):
		w = int((self.width - marge * 2) / grid)
		h = int((self.height - marge * 2) / grid)
		for i, node in enumerate(self.nodes):
			self.nodes[i]["x"] = marge + node["x"] * w
			self.nodes[i]["y"] = marge + node["y"] * h

	def posNodesI(self):
		maxX = 0
		maxY = 0
		y = {}
		history = {}
		for i in range(2):
			for link in self.links:
				if link[i] not in history:
					a = self.nodes[link[i]]
					beforeA = self.linkDeep(link[i], 0) - 1
					a["x"] = beforeA
					X = str(beforeA)
					if X in y:
						y[X] += 1
					else:
						y[X] = 0
					a["y"] = y[X]
					history[link[i]] = True
					if beforeA > maxX:
						maxX = beforeA
					if y[X] > maxY:
						maxY = y[X]
		return maxX if maxX > maxY else maxY


	def linkDeep(self, node, direction):
		ret = 1
		max = 0
		for link in self.links:
			if link[direction] == node:
				tmp = self.linkDeep(link[1 - direction], direction)
				if tmp > max:
					max = tmp
		return ret + max

	# def posNodesI(self, matriceLink):
	# 	size = len(matriceLink)
	# 	liste = []
	# 	# print(matricePos)
	# 	for i in range(size):
	# 		linkBefore = []
	# 		linkAfter = []
	# 		for j in range(size):
	# 			if matriceLink[j][i] == 1:
	# 				linkAfter.append(j)
	# 			if matriceLink[i][j] == 1:
	# 				linkBefore.append(j)
	# 		liste.append({"before": linkBefore, "after": linkAfter})
	# 		print(self.graph["idict"][i], "before", linkBefore, "after", linkAfter)
	# 	print(liste)
	# 	print("travel after", self.travel(liste, 0, "after"))
	# 	print("travel before", self.travel(liste, 5, "before"))
	# 	return 

	# def travel(self, list, i, name):
	# 	# print("travel", i)
	# 	ret = [i]
	# 	for node in list[i][name]:
	# 		ret.append(self.travel(list, node, name))
	# 	return ret


	def getNodes(self):
		return self.nodes

	def getLinks(self):
		links = []
		for link in self.links:
			links.append([self.nodes[link[0]], self.nodes[link[1]]])
		return links

