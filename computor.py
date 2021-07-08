#!/usr/bin/env python3

import sys

def pargs():
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")

def hasdigits(s):
    return(bool(set('0123456789').intersection(s)))

def validnumber(s):
    i = 0
    if s[0] == '-': #|| s[0] == '+':
        i = 1;
    for i in range(i, len(s)):
        if s[i] not in "0123456789":
            break
    if s[i] == '.':
        i = i + 1
    for i in range(i, len(s)):
        if s[i] not in "0123456789":
            break
    return(i == len(s) - 1)

def coefficients(eq):
    coef = {}
    right = False
    #print(eq)
    for n in eq:
        if not '=' in n:
            if not "X" in n:
                c = 0
            elif not "^" in n:
                c = 1
            else:
                c = int(n[n.index('^')+1])
            #print(f"{n}")
            if not '*' in n:
                if n[0] in "0123456789":
                    val = float(n.split("X")[0])
                else:
                    val = 1
            else:
                if validnumber(n.split('*')[0]):
                    val = float(n.split("*")[0])
                elif validnumber(n.split('*')[1]):
                    val = float(n.split("*")[1])
                else:
                    print(f"Invalid value: '{n}' has no valid number")
            if right: val = -val
            if c in coef.keys():
                coef[c] = coef[c] + val
            else:
                coef[c] = val
        else:
            right = True
    return(coef)

def reduced(coef):
    red = ""
    for c in range(max(coef.keys()), -1, -1):
        if not (c in coef.keys()):
            continue
        n = coef[c]
        if n != 0:
            if len(red) > 0:
                if n < 0:
                    red = red + " - "
                    n = -n
                else:
                    red = red + " + "
            if n != 1:
                red = red + f"{n:g}"
            if c >= 1:
                red = red + "X"
            if c > 1:
                red = red + f"^{c}"
    red = red + " = 0"
    return(red)

def degree(coef):
    for i in range(len(coef), 0, -1):
        if (i in coef.keys() and coef[i] != 0):
            return i

def main():
    eq = sys.argv[1]
    eq = eq.replace(" ", "").replace("-", "+-").replace("=", "+=+").strip("+").upper().split("+")
    coef = coefficients(eq)
    red = reduced(coef)
    print(f"Reduced form: {red}")
    d = degree(coef)
    print(f"Polynomial degree: {d}")
    #print(coef)

if __name__ == "__main__":
    main()
