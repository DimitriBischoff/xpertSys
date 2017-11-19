def sym_and(x, matrix, results, indexes):
    links = [i for i, y in enumerate(matrix[x]) if y == 1]
    res = None
    if not links:
        return results[x]
    for z in range(len(links)):
        results[links[z]] = run_through(links[z], matrix, results, indexes)
        if res is not None:
            res = res & results[links[z]]
        else:
            res = results[links[z]]
    return res

def sym_xor(x, matrix, results, indexes):
    links = [i for i, y in enumerate(matrix[x]) if y == 1]
    res = None
    if not links:
        return results[x]
    for z in range(len(links)):
        results[links[z]] = run_through(links[z], matrix, results, indexes)
        if res is not None:
            res = res ^ results[links[z]]
        else:
            res = results[links[z]]
    return res

def sym_not(x, matrix, results, indexes):
    links = [i for i, y in enumerate(matrix[x]) if y == 1]
    res = None
    if not links:
        return results[x]
    for z in range(len(links)):
        results[links[z]] = run_through(links[z], matrix, results, indexes)
        if res is not None:
            res = res | results[links[z]]
        else:
            res = results[links[z]]
    return 0 if res == 1 else 1

def sym_or(x, matrix, results, indexes):
    links = [i for i, y in enumerate(matrix[x]) if y == 1]
    res = None
    if not links:
        return results[x]
    for z in range(len(links)):
        results[links[z]] = run_through(links[z], matrix, results, indexes)
        if res is not None:
            res = res | results[links[z]]
        else:
            res = results[links[z]]
    return res

def run_through(x, matrix, results, indexes):
    if results[x]== 1 and indexes[x][0] != '!':
        return 1
    if indexes[x][0] == '+':
        return sym_and(x, matrix, results, indexes)
    elif indexes[x][0] == '^':
        return sym_xor(x, matrix, results, indexes)
    elif indexes[x][0] == '!':
        return sym_not(x, matrix, results, indexes)
    else:
        return sym_or(x, matrix, results, indexes)

def browse(matrix, inits, indexes):
    results = inits
    for x in range(len(matrix[0])):
        results[x] = run_through(x, matrix, results, indexes)
    return results