#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import sys
from read import *
from graph import *
from graph_window import *
from browse_graph import *

def main(path, showGraph = False):
	results = []
	endstr = ""
	window = None
	try:
		rules, facts, queries = read_run(path)
	except Exception as e:
		print(e)
		return
	graph = Graph(rules)
	if not graph.loop:
		graph.init(facts)
		if showGraph:
			window = GraphShow(graph.getGraph())
		results = browse(graph.matrice, graph.liste, graph.invDictionnaire)
		for i, x in enumerate(queries):
			for y, z in enumerate(graph.invDictionnaire):
				if z == x:
					endstr += "{}result of {} is {}".format("" if not i else "\n", x, results[y])
		print(endstr)
		if window is not None:
			window.loop()
	else:
		print("error graph loop")

if __name__ == '__main__':
	if len(sys.argv) > 1:
		for path in sys.argv[1:]:
			if path != "-g":
				main(path, "-g" in sys.argv)
	else:
		print("error arguments")

