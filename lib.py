#!/usr/bin/python3.4
#-*- coding: utf-8 -*-

def pause():
	input("PAUSE...")

def debug(*params):
	print(*params)
	pause()

def map(tab, f):
	tmp = tab[:]

	for i, elem in enumerate(tmp):
		tmp[i] = f(elem)
	return tmp

def maprecurse(tab, f):
	tmp = []

	for elem in tab:
		if isinstance(elem, list):
			tmp.append(maprecurse(elem, f))
		else:
			tmp.append(f(elem))
	return tmp

def search(tab, l):
	for i in range(len(tab)):
		if tab[i] == l:
			return i
	return -1

def removeall(list, rm):
	while rm in list:
		list.remove(rm)
	return list

def replacesup(s, tab):
	tmp = s

	for i, a in enumerate(tab[0]):
		tmp = tmp.replace(a, tab[1][i])
	return tmp

def splitrules(str, rules, save = False):
	i = 0
	tmp = []

	for j in range(len(str)):
		for rule in rules:
			length = len(rule)
			tmp2 = str[j:j + length]
			if tmp2 == rule:
				tmp.append(str[i:j])
				if save:
					tmp.append(str[j: j + length])
				i = j + length
	tmp.append(str[i:])
	return tmp

def copieMatrice(m):
	mTmp = []
	for l in m:
		mTmp.append(l[:])
	return mTmp