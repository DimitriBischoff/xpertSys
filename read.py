# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    read.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rmicolon <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2017/10/12 15:54:54 by rmicolon          #+#    #+#              #
#    Updated: 2018/02/21 16:52:22 by rmicolon         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

#TODO:
# errors : 
#  - request for non existing letter
#  - parenthesis correctness
#  - plusieurs signes '='
#  - check espaces
#  - check ordre parametres ?
#  - check symbol correctness ('avec string harcodee degueu')
#  - check symbol on right side 


LOK = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ' + '!+|^' + '=()'
ROK = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ' + '!+' 

def error(str):
    print('Error: {}'.format(str))
    exit(1)


def formatRule(rule, errule, p, eq):
    lst = []
    while rule:
        if (eq == 0 and rule[0] not in LOK) or (eq == 1 and rule[0] not in ROK):
            error('Wrong symbol {0} in rule "{1}"'.format(rule[0], " ".join(errule)))
        elif rule[0] == '=':
            if rule[1] == '>':
                lst.append("".join(rule[0:2])) if p == 0 else error('Parenthesis error in rule "{0}"'.format(" ".join(errule)))
                eq = 1
                del rule[0:2]
            else:
                error('Wrong symbol {0} in rule "{1}"'.format(rule[0:1], errule))
        elif rule[0] == '(':
            del rule[0]
            lst.append(formatRule(rule, errule, p+1, eq))
        elif rule[0] == ')':
            del rule[0]
            return (lst) if p > 0 else error('Parenthesis error in rule "{0}"'.format(" ".join(errule)))
        else:
            lst.append(rule[0])
            del rule[0]
    return lst 


def cleanInput(input):
    queries = None
    facts = None
    lst = list(filter(None, map(lambda x: x.split('#', 1)[0].strip(), input.replace(" ", "").splitlines())))
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
    for rule in rules:
        if "=>" not in rule:
            error('No implication sign in rule "{0}"'.format(" ".join(rule)))
    return rules, facts, queries


def read_input(name):
    with open(name, 'r') as fo:
        input = fo.read()
    return(input)


def read_run(path):
    input = read_input(path)
    rules, facts, queries = cleanInput(input)
    rules = [ formatRule(list(rule), rule, 0, 0) for rule in rules ]
    return rules, facts, queries

