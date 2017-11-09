#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from graph import *
from graph_window import *

code = [
	# ["!", "B", "+", ["D", "|", "A"], "=>", "C", "+", "Z"],
	# ["!", "A", "=>", "!", "B"],
	# ["C", "=>" ,"E"],
	# ["A" ,"+" ,"B" ,"+" ,"C" ,"=>" ,"D"],
	# ["A" ,"|" ,"B" ,"=>" ,"C"],
	# ["A" ,"+" ,"!", "B" ,"=>" ,"F"],
	# ["C" ,"|" ,"!", "G" ,"=>" ,"H"],
	# ["V" ,"^" ,"W" ,"=>" ,"X"],
	# ["A" ,"+" ,"B" ,"=>" ,"Y" ,"+" ,"Z"],
	# ["C" ,"|" ,"D" ,"=>" ,"X" ,"|" ,"V"],
	# ["E" ,"+" ,"F" ,"=>" ,"!" ,"V"],
	["B", "=>", "A"], 
	["D", "+", "E", "=>", "B" ],
	["G", "+", "H", "=>", "F" ],
	["I", "+", "J", "=>", "G" ],
	["G", "=>", "H", ],
	["L", "+", "M", "=>", "K" ],
	["O", "+", "P", "=>", "L", "+", "N" ],
	["N", "=>", "M", ],
]
init = "A"
query = "E"

def main():
	# print([0] * 2)
	graph = Graph(code)
	# print(graph)
	graph.init(init)
	window = GraphShow(graph.getGraph())
	print(graph)
	window.loop()
	# print(graph.query(query))

main()
