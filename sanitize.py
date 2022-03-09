def validcompnum(n, i, nlen):
    starti = i
    if n[i] in "-":
        i = i + 1
    while i < nlen and n[i] in "0123456789":
        i = i + 1
    if i < nlen and n[i] == ".":
        i = i + 1
        if i == nlen or n[i] not in "0123456789":
            return False
        while i < nlen and n[i] in "0123456789":
            i = i + 1
    if i < nlen and n[i] == "X":
        i = i + 1
        if i < nlen and n[i] == "^":
            i = i + 1
            if i == nlen or n[i] not in "0123456789":
                return False
            while i < nlen and n[i] in "0123456789":
                i = i + 1
    if starti == i:
        return False
    return i


def validcomp(n):
    i = 0
    nlen = len(n)
    i = validcompnum(n, i, nlen)
    if not i:
        return False
    while i < nlen and n[i] == "*":
        i = i + 1
        if not i < nlen:
            return False
        i = validcompnum(n, i, nlen)
    return i == nlen


def sanitize(eq):
    right = False
    eq = list(
        filter(
            None,
            eq.replace(" ", "")
            .replace("x", "X")
            .replace("-", "+-")
            .replace("=", "+=+")
            .strip("+")
            .split("+"),
        )
    )
    i = 0
    for n in eq:
        if n == "=":
            if i == 0:
                print(f"Error: invalid equation (nothing before equal sign)")
                return False
            if right:
                print(f"Error: invalid equation (more than one equal sign)")
                return False
            right = True
        elif not validcomp(n):
            print(f"Error at '{n}': parsing failed")
            return False
        i = i + 1
    if not right:
        print("Error: not an equation (missing equal sign)")
        return False
    if eq[i - 1] == "=":
        print("Error: invalid equation (nothing after equal sign)")
        return False
    return eq
