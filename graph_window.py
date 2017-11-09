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
		self.posNodesRand()

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

	def posNodeI(self):
		return

	def getNodes(self):
		return self.nodes

	def getLinks(self):
		links = []
		for link in self.links:
			links.append([self.nodes[link[0]], self.nodes[link[1]]])
		return links

