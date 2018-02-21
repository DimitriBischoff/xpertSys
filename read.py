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
import re

#TODO:
# errors : 
#  - parenthesis correctness
#  - plusieurs signes '='
#  - check espaces
#  - check ordre parametres ?
#  - check symbol correctness ('avec string harcodee degueu')
#  - check symbol on right side 


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

def errorCode(code):
    errors = []
    regex = r"([A-Z]{2,})|([+^|]{2,})|([+^|]=>)|([^A-Z+|^=>()!\n])|(!!)|((>|^)[+|^])|(={2,})|(>{2,})|(![+|^])|(=>.+[|^])"
    for i, l in enumerate(code):
        e = re.search(regex, l)
        if e:
            errors.append("%-5i: wrong symbole { %s } in rule %s" % (i, e.group(0), e.string))
    return None if not errors else errors

def cleanInput(input):
    queries = None
    facts = None

    lst = list(filter(None, map(lambda x: x.split('#', 1)[0].strip(), input.replace(" ", "").splitlines())))
    error = errorCode(lst[:-2])
    if error:
        raise Exception("\n".join(str(i) for i in error))
    else:
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
    with open(name, 'r') as fo:
        input = fo.read()
    return(input)

def read_run(path):
    input = read_input(path)
    rules, facts, queries = cleanInput(input)
    rules = [ formatRule(list(rule), 0) for rule in rules ]
    return rules, facts, queries

if __name__ == '__main__':
    # for arg in sys.argv[1:]:
    rules, facts, queries = read_run("test")
    print(rules, facts, queries)

