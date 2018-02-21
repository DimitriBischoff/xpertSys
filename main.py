#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import sys
from read import *
from graph import *
from graph_window import *
from browse_graph import *

def main(path):
	results = []
	endstr = ""
	try:
		rules, facts, queries = read_run(path)
	except IOError:
		print("error file", path)
		return
	graph = Graph(rules)
	if not graph.loop:
		graph.init(facts)
		window = GraphShow(graph.getGraph())
		results = browse(graph.matrice, graph.liste, graph.invDictionnaire)
		for i, x in enumerate(queries):
			for y, z in enumerate(graph.invDictionnaire):
				if z == x:
					endstr += "{}result of {} is {}".format("" if not i else "\n", x, results[y])
		print(endstr)
		window.loop()
	else:
		print("error graph loop")

if __name__ == '__main__':
	if len(sys.argv) > 1:
		for path in sys.argv[1:]:
			main(path)
	else:
		print("error arguments")
