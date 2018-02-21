#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from graph import *
from graph_window import *
from browse_graph import *

code = [
	["A", "=>", "C"],
	["C", "=>", "D"],
	# ["D", "=>", "C"],
]
# init = ["A", "B", "G"]
init = "A"
query = "C"

def main():
	results = []
	endstr = "" 
	# print([0] * 2)
	graph = Graph(code)
	print(graph, graph.loop)
	if not graph.loop:
		graph.init(init)
		window = GraphShow(graph.getGraph())
		#print(graph.matrice)
		# results = browse(graph.matrice, graph.liste, graph.invDictionnaire)
		# for x in query:
		#	for y, z in enumerate(graph.invDictionnaire):
		#		if z == x:
		#		endstr += "result of {} is {}\n".format(x, results[y])
		# print(endstr)
		window.loop()
		# print(graph.query(query))

main()

