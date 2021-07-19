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
    if s[0] == '-':# || s[0] == '+':
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

def parsenum(n):
    val = 1
    if not '𝓍' in n:
        c = 0
        val = float(n)
    else:
        if n[0] == '-' and n[1] == '𝓍':
            val = -1
        elif n[0] != '𝓍':
            val = float(n.split("𝓍")[0])
        if not '^' in n:
            c = 1
        else:
            c = int(n[n.index('^')+1])
    return (val, c)

def coefficients(eq):
    coef = {}
    right = False
    for n in eq:
        if not '=' in n:
            val = 1
            exp = 0
            for part in n.split('*'):
                (v, c) = parsenum(part)
                val = v * val
                exp = c + exp
            if right:
                val = -val
            if exp in coef.keys():
                coef[exp] = coef[exp] + val
                if coef[exp] == 0:
                    del coef[exp]
            else:
                coef[exp] = val
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
            if n != 1 or c == 0:
                if n == -1:
                    red = "-"
                else:
                    red = red + f"{n:g}"
            if c >= 1:
                red = red + "𝓍"
            if c > 1:
                red = red + f"^{c}"
    red = red + " = 0"
    return(red)

def degree(coef):
    if len(coef) > 0:
        return max(k for k, v in coef.items())
    return 0

def check(coef, d):
    if d == 0:
        if 0 not in coef.keys() or coef[0] == 0:
            print("This equation is always true.")
        else:
            print("This equation has no solution.")
        return (False)
    return (True)

def validcompnum(n, i, l):
    starti = i
    if n[i] in "-":
        i = i + 1
    while i < l and n[i] in "0123456789":
        i = i + 1
    if i < l and n[i] == '.':
        i = i + 1
        if  i == l or n[i] not in "0123456789":
            return False
        while i < l and n[i] in "0123456789":
            i = i + 1
    if  i < l and n[i] == '𝓍':
        i = i + 1
        if i < l and n[i] == '^':
            i = i + 1
            if  i == l or n[i] not in "0123456789":
                return False
            while i < l and n[i] in "0123456789":
                i = i + 1
    if starti == i:
        return False
    return (i)

def validcomp(n):
    i = 0
    l = len(n)
    i = validcompnum(n, i, l)
    if not i:
        return (False)
    while i < l and n[i] == '*':
        i = i + 1
        if not i < l:
            return (False)
        i = validcompnum(n, i, l)
    return (i == l)

def sanitize(eq):
    right = False
    eq = list(filter(None, eq.replace(" ", "").replace('x', '𝓍').replace("-", "+-").replace("=", "+=+").strip("+").split("+")))
    i = 0
    for n in eq:
        if n == '=':
            if i == 0:
                print(f"Error: invalid equation (nothing before equal sign)")
                return False
            if right == True:
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
    if eq[i-1] == '=':
        print("Error: invalid equation (nothing after equal sign)")
        return False
    return eq

def gcd(n1, n2):
    if n1 < n2:
        (n1,n2) = (n2,n1)
    if n1 % n2 == 0:
        return (n2)
    return (gcd(n2, n1 % n2))

def frac(n1, n2):
    if n1 % n2 == 0:
        return (f"{(n1/n2):g}")
    g = gcd(n1,n2)

    n1 = n1 // g
    n2 = n2 // g
    if n2 < 0:
        n1 = -n1
        n2 = -n2
    return (f"{n1:g}/{n2:g}")

def sqrt(n):
    pass

def solve1(coef):
    print("The solution is:")
    if coef[0] == 0:
        print("𝓍 = 0")
    else:
        print("𝓍 = " + frac(-coef[0], coef[1]))

def solve2(coef):
    a = 0 if not 2 in coef.keys() else coef[2]
    b = 0 if not 1 in coef.keys() else coef[1]
    c = 0 if not 0 in coef.keys() else coef[0]
    delta = b*b-4*a*c
    print(f"a = {a} ; b = {b}  ; c = {c}")
    print(f"delta = {delta}")
    if delta < 0:
        print("Discriminant is strictly negative, I can't solve for the moment.") #𝒾
    elif delta == 0:
        print(f"Discriminant is zero, the solution is:\n{frac(-b, 2*a)}")
    else:
        print("Discriminant is strictly positive, the two solutions are:")
        print(f"({-b:g} - √{delta:g}) / {2*a:g}")
        print(f"({-b:g} + √{delta:g}) / {2*a:g}")

def main():
    eq = sys.argv[1]
    eq = sanitize(eq)
    #print(eq)
    if eq == False: return
    coef = coefficients(eq)
    d = degree(coef)
    if (not check(coef, d)):
        return
    red = reduced(coef)
    if red[0] == '-':
        coef = coefficients(sanitize("0 = " + red.split('=')[0].strip()))
        red = reduced(coef)
    #print(eq)
    print(f"Reduced form: {red}")
    d = degree(coef)
    print(f"Polynomial degree: {d}")
    if d == 1:
        solve1(coef)
    elif d == 2:
        solve2(coef)
    elif d > 2:
        print(f"The polynomial degree is stricly greater than 2, I can't solve.")

if __name__ == "__main__":
    main()
