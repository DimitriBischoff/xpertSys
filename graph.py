#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

def stringMatrix(matrix, legende = [], sepChar = ", ", sepLine = "\n"):
	tmpLegende = []
	for char in legende:
		tmpLegende.append(char[:1])
	tmpMatrix = ["   " + "  ".join(tmpLegende)] if len(tmpLegende) > 0 else []
	for i, line in enumerate(matrix):
		tmpLine = [tmpLegende[i]] if i < len(tmpLegende) else []
		for char in line:
			tmpLine.append(str(char))
		tmpMatrix.append(sepChar.join(tmpLine))
	return sepLine.join(tmpMatrix)

class Graph:

	def __init__(self, code):
		self.dictionnaire = {}
		self.invDictionnaire = []
		self.liste = []
		self.matrice = []
		tmpCode = self.renameOp(code)
		self.travelCode(tmpCode)

	def __str__(self):
		print(self.dictionnaire)
		print(self.liste)
		print(self.invDictionnaire)
		return stringMatrix(self.matrice, self.invDictionnaire, "  ")

	def renameOp(self, code, nb = []):
		prio = "!+|^"
		if len(nb) < len(prio):
			nb = [1] * len(prio)

		for line in code:
			for i, char in enumerate(line):
				for iop, op in enumerate(prio):
					if isinstance(char, list):
						line[i] = self.renameOp([char], nb)[0]
					elif char == op:
						line[i] = char + str(nb[iop])
						nb[iop] += 1
		return code

	def getChar(self, line, i):
		if i >= 0 and i < len(line):
			if isinstance(line[i], list):
				return self.travelStart(line[i])
			else:
				return line[i]
		return ""

	def indexArrow(self, line):
		for i, char in enumerate(line):
			if "=>" in char:
				return i
		return -1

	def travelCode(self, code):
		for line in code:
			arrow = self.indexArrow(line)
			start = line[:arrow]
			end = line[arrow + 1:]
			op = self.travelStart(start)
			self.travelEnd(end, op)

	def travelEnd(self, line, opOld):
		opPrio = "!+|^"
		i = 0
		while i < len(line):
			char = line[i]
			for op in opPrio:
				if op in char:
					if "!" in char:
						self.addLink(char, self.getChar(line, i + 1))
						del line[i + 1]
					else:
						self.addLink(char, self.getChar(line, i - 1))
						self.addLink(char, self.getChar(line, i + 1))
						del line[i]
						i -= 1
			i += 1
		for char in line:
			self.addLink(opOld, char)


	def travelStart(self, line):
		opMax = ""
		opPrio = "!+|^"
		if len(line) == 1:
			opMax = self.getChar(line, 0)
		for op in opPrio:
			for i, char in enumerate(line):
				if isinstance(char, str) and op in char:
					line = self.creaNode(line, i)
					if opMax == "" and op != "!":
						opMax = char

		return opMax

	def creaNode(self, line, i):
		a = self.getChar(line, i-1)
		op = line[i]
		b = self.getChar(line, i+1)
		if b != "":
			self.addLink(b, op)
			del line[i+1]
		if "!" not in op and a != "":
			self.addLink(a, op)
			del line[i-1]
		return line

	def exist(self, node):
		return node in self.dictionnaire

	def getIndex(self, node):
		return self.dictionnaire[node] if self.exist(node) else -1

	def setValue(self, node, value):
		if self.exist(node):
			self.liste[self.getIndex(node)] = value
		else:
			self.addNode(node)
			self.setValue(node, value)
	
	def getValue(self, node):
		if self.exist(node):
			return self.liste[self.getIndex(node)]
		else:
			self.addNode(node)
			return self.getValue(node)

	def getNode(self, index):
		return self.invDictionnaire[index]

	def addNode(self, node):
		if not self.exist(node) and len(node):
			self.dictionnaire[node] = len(self.liste)
			self.invDictionnaire.append(node)
			self.liste.append(0)
	
			if len(self.matrice) == 0:
				self.matrice = [[0]]
			else:
				self.matrice.append([0] * len(self.matrice))
				for i, line in enumerate(self.matrice):
					self.matrice[i] += [0]
			return True
		elif self.exist(node):
			return True
		return False

	def addLink(self, node1, node2):
		if self.exist(node1) and self.exist(node2):
			print("link", node1, node2)
			index1 = self.getIndex(node1)
			index2 = self.getIndex(node2)
			self.matrice[index2][index1] = 1
		elif self.addNode(node1) and self.addNode(node2):
			self.addLink(node1, node2)

	def getGraph(self):
		return {
			"dict"	: self.dictionnaire,
			"idict"	: self.invDictionnaire,
			"list"	: self.liste,
			"matrix": self.matrice
		}

	def init(self, init):
		for char in init:
			self.setValue(char, 1)

