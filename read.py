# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    read.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rmicolon <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2017/10/12 15:54:54 by rmicolon          #+#    #+#              #
#    Updated: 2018/02/08 22:57:46 by rmicolon         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

#TODO:
# errors : 
#  - parenthesis correctness
#  - plusieurs signes '='
#  - check espaces
#  - check ordre parametres ?
#  - check symbol correctness ('avec string harcodee degueu')
#  - check symbol on right side 


class ruleside:
    def __init__(self, string):
        self.rule = string.replace(' ','')
    
    def contains(self, char):
        if self.rule.count(char):
            return True
        return False

class rule:
    def __init__(self, string):
        self.strule = string
        if string.count('<=>'):
            self.sign = 1
            self.left = ruleside(string.split('<=>')[0])
            self.right = ruleside(string.split('<=>')[1])
        elif string.count('=>'):
            self.sign = 0
            self.left = ruleside(string.split('=>')[0])
            self.right = ruleside(string.split('=>')[1])
        self.check()


    def perror(self, string):
        print(string)
        sys.exit()

    def check(self):
        if self.sign == 1:
            if self.left.rule.count('(') or self.left.rule.count(')') or \
                self.right.rule.count('(') or self.right.rule.count(')'):
                    self.perror('target in rule : "' + self.strule + '" contains parenthesis')
            elif self.left.rule.count('|') or self.righ.rule.count('|'):
                self.perror('target in rule : "' + self.strule + '" contains OR sign')
            elif self.left.rule.count('^') or self.righ.rule.count('^'):
                self.perror('target in rule " ' + self.strule + '" contains XOR sign')
        elif self.sign == 0:
            if self.right.rule.count('(') or self.right.rule.count(')'):
                self.perror('target in rule : "' + self.strule + '" contains parenthesis')
            elif self.right.rule .count('|'):
                self.perror('target in rule : "' + self.strule + '" contains OR sign')
            elif self.right.rule.count('^'):
                self.perror('target in rule : "' + self.strule + '" contains XOR sign')
            

    def evaluate(self, facts, item):
        nope = 0
        ret = 0
        if type(item) is int:
            ret = item
        else:
            if item[0] == '!':
                nope = 1
            if (len(item) > 2 and nope == 1) or (len(item) > 1 and nope == 0):
                ret = self.resolve(ruleside(item), facts)
            else:
                if facts.count(item):
                    ret = 1
                else:
                    ret = 0
        if ret == 0:
            return nope
        else:
            return ret - nope

    def mand(self, facts, a, op, b):
        tmpa = a
        tmpb = b
        tmpop = op
        a = self.evaluate(facts, a)
        b = self.evaluate(facts, b)
        print('result of ', tmpa, tmpop, tmpb, ' = ', a & b)
        return a & b

    def mor(self, facts, a, op, b):
        tmpa = a
        tmpb = b
        tmpop = op
        a = self.evaluate(facts, a)
        b = self.evaluate(facts, b)
        print('result of ', tmpa, tmpop, tmpb, ' = ', a | b)
        return a | b

    def mxor(self, facts, a, op, b):
        tmpa = a
        tmpb = b
        tmpop = op
        a = self.evaluate(facts, a)
        b = self.evaluate(facts, b)
        print('result of ', tmpa, tmpop, tmpb, ' = ', a ^ b)
        return a ^ b

    def split(self, string):
        j = 0
        p = 0
        tab = [['' for x in range(len(string))] for y in range(2)]
        signs = '+|^'
        for i in range(len(string)):
            if string[i] == '(':
                p += 1
                if p > 1:
                    tab[0][j] = tab[0][j] + string[i]
            elif string[i] == ')':
                if p > 1:
                    tab[0][j] = tab[0][j] + string[i]
                p -= 1
            elif signs.count(string[i]) and p == 0:
                tab[1][j] = string[i]
                j += 1
            else:
                tab[0][j] = tab[0][j] + string[i]
        tab[0] = list(filter(None, tab[0]))
        tab[1] = list(filter(None, tab[1]))
        return tab

    def resolve(self, side, facts):
        tab = self.split(side.rule)
        print('split = ', tab)
        i = 0
        while len(tab[1]) > 0:
            if (tab[1].count('+') and i == tab[1].index('+')):
                tab[0][i] = self.mand(facts, tab[0][i], tab[1][i], tab[0][i+1])
                del tab[1][i]
                del tab[0][i+1]
            elif (tab[1].count('|') and i == tab[1].index('|')):
                tab[0][i] = self.mor(facts, tab[0][i], tab[1][i], tab[0][i+1])
                del tab[1][i]
                del tab[0][i+1]
            elif (tab[1].count('^') and i == tab[1].index('^')):
                tab[0][i] = self.mxor(facts, tab[0][i], tab[1][i], tab[0][i+1])
                del tab[1][i]
                del tab[0][i+1]
        return (tab[0][0])

OK = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ' + '!+-|^' + '=()'

def error(str):
    print('Error: {}'.format(str))
    exit(1)


def formatRule(rule, p):
    lst = []
    errule = list(rule)
    while rule:
        if rule[0] not in OK:
            error('Wrong symbol {0} in rule "{1}"'.format(rule[0], errule))
        elif rule[0] == '=':
            if rule[1] == '>':
                lst.append("".join(rule[0:2]))
                del rule[0:2]
            else:
                error('Wrong symbol {0} in rule "{1}"'.format(rule[0:1], errule))
        elif rule[0] == '(':
            del rule[0]
            lst.append(formatRule(rule, p+1))
        elif rule[0] == ')':
            del rule[0]
            return (lst) if p > 0 else error('Parenthesis error in rule "{0}"'.format(errule))
        else:
            lst.append(rule[0])
            del rule[0]
    return lst 


def cleanInput(input):
    queries = None
    facts = None
    lst = list(filter(None, map(lambda x: x.split('#', 1)[0].strip(), input.splitlines())))
    rules = list(lst)
    for j in range(len(lst)):
        if lst[j][0] == '?':
            if queries is not None:
                error('Multiple queries statement')
            queries = lst[j][1:]
            rules.remove(lst[j])
        elif lst[j][0] == '=':
            if facts is not None:
                error('Multiple facts statement')
            facts = lst[j][1:]
            rules.remove(lst[j])
    return rules, facts, queries


def read_input(name):
    fo = open(name, 'r')
    input = fo.read()
    fo.close()
    return(input)


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        input = read_input(arg)
        rules, facts, queries = cleanInput(input)
        rules = [ formatRule(list(rule), 0) for rule in rules ]
        print(rules)

