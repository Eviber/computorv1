#!/usr/bin/env python3

import sys

def pargs():
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")

def coefficients(eq):
    coef = {}
    right = False
    print(eq)
    for n in eq:
        if not '=' in n:
            if not "X" in n:
                c = 0
            elif not "^" in n:
                c = 1
            else:
                c = int(n[n.index('^')+1])
            #print(f"{n[n.index('^')+1]} {n}")
            if not '*' in n:
                val = float(n.split("X")[0])
            else:
                val = float(n.split("*")[0])
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
        n = coef[c]
        if n != 0:
            if len(red) > 0:
                if n < 0:
                    red = red + " - "
                    n = -n
                else:
                    red = red + " + "
            red = red + f"{n:g}"
            if c >= 1:
                red = red + "X"
            if c > 1:
                red = red + f"^{c}"
    return(red)

def main():
    eq = sys.argv[1]
    eq = eq.replace(" ", "").replace("-", "+-").replace("=", "+=+").strip("+").split("+")
    coef = coefficients(eq)
    red = reduced(coef)
    print(f"Reduced form: {red}")
    #print(f"Equation de degré {d}")
    #print(coef)

if __name__ == "__main__":
    main()
