#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import sys
from read import *
from graph import *
from graph_window import *
from browse_graph import *

def main(path, showGraph = False):
	results = []
	str = ""
	window = None
	try:
		rules, facts, queries = read_run(path)
	except IOError:
		print("error file", path)
		return
	graph = Graph(rules)
	if not graph.loop:
            graph.init(facts)
            if showGraph:
                window = GraphShow(graph.getGraph())
            results = browse(graph.matrice, graph.liste, graph.invDictionnaire)
            if queries:
                for i, x in enumerate(queries):     
                    for y, z in enumerate(graph.invDictionnaire):
                        if z == x:
                            str = "result of {} is {}".format(x, bool(results[y]))
                    print(str) if str else print("result of {} is {}".format(x, False))
                    str = ""
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
