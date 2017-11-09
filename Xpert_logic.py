# init = ["B"]
# answer = ["C", "D"]
# code = [["!", "A", "|", "B", "+", "!", ["A", "+", "B"], "=>", "C", "|", "D"]]
code = [
["C", "=>" ,"E"],
["A" ,"+" ,"B" ,"+" ,"C" ,"=>" ,"D"],
["A" ,"|" ,"B" ,"=>" ,"C"],
["A" ,"+" ,"!", "B" ,"=>" ,"F"],
["C" ,"|" ,"!", "G" ,"=>" ,"H"],
["V" ,"^" ,"W" ,"=>" ,"X"],
["A" ,"+" ,"B" ,"=>" ,"Y" ,"+" ,"Z"],
["C" ,"|" ,"D" ,"=>" ,"X" ,"|" ,"V"],
["E" ,"+" ,"F" ,"=>" ,"!" ,"V"]
]
init = ["A", "B", "G"]
answer = ["G", "V", "X"] 

class Logic:

	def __init__(self, init, answer, instructions):
		self.memory = [False] * 26
		self.init = init
		self.answer = answer
		self.instructions = instructions

		for char in init:
			self.setMem(char, True)
		self.resolve()

	def __str__(self):
		return ("={}\n?{}\n{}").format(self.init, self.answer, self.memory)

	# -- Memory --

	def charCode(self, letter):
		if self.isLetter(letter):
			return ord(letter) - ord('A')
		else:
			return -1

	def setMem(self, letter, value):
		index = self.charCode(letter)

		if index >= 0:
			self.memory[index] = value

	def getMem(self, letter):
		index = self.charCode(letter)

		if index >= 0:
			return self.memory[index]
		else:
			False

	# -----------

	def isLetter(self, letter):
		return letter >= 'A' and letter <= 'Z'

	def resolve(self):
		for inst in self.instructions:
			index = inst.index("=>")
			debut = inst[:index]
			fin = inst[index + 1:]
			self.value(fin, self.solution(debut))

	def value(self, code, solution):
		i = 0

		if len(code) == 1:
			self.setMem(code[0], solution)
		elif solution == True:
			if "|" not in code and "^" not in code:
			 	while i < len(code):
					if code[i] == "!" and i + 1 < len(code):
						self.setMem(code[i + 1], not solution)
						i += 1
					elif self.isLetter(code[i]):
						self.setMem(code[i], solution)
					i += 1
		print("value", code, solution)

	def solution(self, code):
		i = 1
		get = lambda code, i: code[i] if i < len(code) else False
		ret = self.getValue(get(code, 0))
		
		if ret == "!":
			ret = not self.getValue(get(code, 1))
			i = 2
		while i < len(code):
			op = self.getValue(get(code, i))
			val = self.getValue(get(code, i + 1))

			if val == "!":
				val = not self.getValue(get(code, i + 2))
				i += 1

			if (type(op) == str):
				ret = self.calc(ret, op, val)
			i += 2
		print("solution", code, ret)
		return ret

	def getValue(self, a):
		# print("getValue", a)
		if isinstance(a, list):
			return self.solution(a)
		elif self.isLetter(a):
			return self.getMem(a)
		else:
			return a


	def calc(self, a, op, b):
		if op in "+|^":
			return {
				"+"	: lambda a, b: a & b,
				"|"	: lambda a, b: a | b,
				"^"	: lambda a, b: a ^ b
			}[op](a, b)
		else:
			print("probleme op", a, op, b)
			return False

	def resultat(self):
		ret = []
		for char in self.answer:
			ret += [[char, self.getMem(char)]]
		return ret


# debug

logic = Logic(init, answer, code)
print(logic)
print(logic.resultat())
# print(logic.charCode('b'))