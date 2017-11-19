#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from graph import *
from graph_window import *
from browse_graph import *

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
init = "DEIJP"
query = "AFKP"

def main():
    results = []
    endstr = ""
    graph = Graph(code)
    graph.init(init)
    window = GraphShow(graph.getGraph())
    #window.loop()
    results = browse(graph.matrice, graph.liste, graph.invDictionnaire)
    print("\nRESULTS:")
    for x in query:
        for y, z in enumerate(graph.invDictionnaire):
            if x == z:
                endstr += "result of {} is {}\n".format(x, results[y])
    print(endstr)

main()
