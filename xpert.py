#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
import sys
from lib import *

class Expert:

	def __init__(self, path):

		self.valid = not self.error(path)
		self.memory = [0] * 26
		self.init = []
		self.facts = []
		self.request = []
		self.linemax = -1
		self.debug = False
		if self.valid:
			self.decompose(self.parse(path))

	def __str__(self):
		border = "-" * 80
		text = "\nmemory\t: {}\ninit\t: {}\nrequest\t: {}\nfacts\t: {}\n"
		
		if not self.valid:
			return self.mess_error
		return (border + text + border).format(
				self.memory,
				map(self.init, self.nl),
				map(self.request, self.nl),
				self.facts)

	def error(self, path):
		if not os.path.exists(path):
			self.mess_error = "File not found."
		elif not os.path.isfile(path):
			self.mess_error = "It's not file."
		else:
			return False
		return True

	def extractletter(self, tab):
		tmp = []

		for l in tab:
			if self.isletter(l):
				tmp.append(self.ln(l))
		return tmp

	def decompose(self, tab):
		i = 0
		while i < len(tab):
			if tab[i][0] == '?':
				self.request = self.extractletter(tab[i])
				del tab[i]
			elif tab[i][0] == '=':
				self.init = self.extractletter(tab[i])
				del tab[i]
			else:
				i += 1
		self.facts = tab

	def parse(self, path):
		tmp = []

		with open(path, "r") as fichier:
			tmp = removeall(map(fichier.read().split("\n"), self.normalise), "")
		return tmp

	def resolve(self, debug = False):
		self.debug = debug
		for i in self.init:
			self.memory[i] = 1
		i = 0
		while i < len(self.facts):
			fact = self.factcut(self.facts[i])
			if not self.factvalid(fact[1]):
				if self.linemax == i:
					self.valid = False
					self.mess_error = "Insolvable."
					return False
				self.linemax = i if i > self.linemax else self.linemax
				if self.factproblem(fact):
					i = 0
			i += 1
		return True

	def factcut(self, fact):
		tmp = []
		dbsens = "<=>" in fact						# False, True | =>, <=>
		rules = ["<=>" if dbsens else "=>", "|", "+", "^", "(", ")"]

		tmp.append(self.parenthese(removeall(splitrules(fact, rules, True), ""))[0])
		tmp.append(maprecurse(tmp[0], lambda a: self.get_memory(a)))
		return tmp

	def factvalid(self, fact):
		equal = (search(fact, "=>") + 1 | search(fact, "<=>") + 1) - 1
		a = self.logic(fact[:equal])
		b = self.logic(fact[equal + 1:])

		return a == b

	def getfactcomplexe(self, fact):
		i = (search(fact[1], "=>") + 1 | search(fact[1], "<=>") + 1) - 1

		return {
			"score": [
				self.logic(fact[1][:i]),
				self.logic(fact[1][i + 1:])
			],
			"factn": [
				fact[1][: i],
				fact[1][i + 1:]
			],
			"factl": [
				fact[0][: i],
				fact[0][i + 1:]
			],
			"dbsens": "<=>" in fact[1][i]
		}

	def factproblem(self, fact):
		cfact = self.getfactcomplexe(fact)
		# debug(cfact)

		if len(cfact["factn"][1]) == 1:
			l = cfact["factl"][1][0]
			n = cfact["score"][0]
			self.set_memory(l, n)
		else:
			ou = search(cfact["factn"][1], '|')
			xou = search(cfact["factn"][1], '^')
 
			if ou == -1 and xou == -1:
				for l in cfact["factl"][1]:
					if self.isletter(l):
						self.set_memory(l, cfact["score"][0])
			else:
				for l in cfact["factl"][1]:
					if self.isletter(l):
						self.set_memory(l, -1)
				return False
		return True

	def parenthese(self, tab, i = 0):
		tmp = []

		while i < len(tab):
			if tab[i] == ")":
				return tmp, i
			elif tab[i] == "(":
				tmp2, i = self.parenthese(tab, i + 1)
				tmp.append(tmp2)
			else:
				tmp.append(tab[i])
			i += 1
		return tmp, i

	def logic(self, tab):
		ret = self.logic(tab[0]) if isinstance(tab[0], list) else tab[0]
		i = 1

		while i + 1 < len(tab):
			if isinstance(tab[i + 1], list):
				# debug(ret, tab[i])
				ret = self.calc(ret, self.logic(tab[i + 1]), tab[i])
			elif tab[i + 1] is "!":
				# debug(ret, tab[i + 1], tab[i + 2])
				ret = self.calc(ret, self.logic(tab[i + 2]), tab[i])
				i += 1
			else:
				# debug(ret, tab[i], tab[i + 1])
				ret = self.calc(ret, tab[i + 1], tab[i])
			i += 2
		# debug(ret)
		return ret		

	def set_memory(self, l, e):
		neg = False
		if len(l) > 1 and l[0] == '!':
			neg = True
			l = l[1]
		if l >= 'A' and l <= 'Z':
			e = 1 - e if neg else e
			if self.debug:
				print("!" if neg else "", l, " = ", e, sep="")
			self.memory[self.ln(l)] = e

	def get_memory(self, l):
		neg = False
		if len(l) > 1 and l[0] == '!':
			neg = True
			l = l[1]
		if l >= 'A' and l <= 'Z':
			tmp = self.memory[self.ln(l)]
			return 1 - tmp if neg else tmp
		return l

	def result(self):
		fct = lambda a: self.memory[a] == 1

		return maprecurse(self.request, fct) if self.valid else self

	def calc(self, a, b, op):
		if a != -1 and b != -1:
			return {
				"+"	: lambda a, b: a & b,
				"|"	: lambda a, b: a | b,
				"^"	: lambda a, b: a ^ b
			}[op](a, b)
		elif a == -1 and b == -1:
			return -1
		elif a == -1 and b != -1:
			a, b = b, a
		if op == "+" and a == 0:
			return 0
		elif op == "|" and a == 1:
			return 1
		return -1

	def print(self):
		result = self.result()

		for fact in self.facts:
			tab = self.factcut(fact)
			for i, elem in enumerate(tab[0]):
				self.printtab(elem)
			print("")
		print("Resutat: ")
		for i, elem in enumerate(self.request):
			print(self.nl(elem), result[i])


	def printtab(self, tab):
		if isinstance(tab, list):
			for i, elem in enumerate(tab):
				self.printtab(elem)
		else:
			print(tab, end='')
			print(' ', end='')

	def normalise(line):
		index = search(line, '#')

		if index is not -1:
			line = line[:index]
		return replacesup(line, [[" ", "\t"], ["", ""]])

	normalise = staticmethod(normalise)
	isletter = staticmethod(lambda l: l >= 'A' and l <= 'Z')
	ln = staticmethod(lambda a: ord(a) - ord('A'))	# letter => number
	nl = staticmethod(lambda a: chr(ord('A') + a))	# number => letter


if __name__ == "__main__":
	for arg in sys.argv[1:] :
		expert = Expert(arg)
		expert.resolve()
		expert.print()

