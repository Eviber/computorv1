#!/usr/bin/env python3

import sys

import parse
from sanitize import sanitize
import solver
from polytools import *


def usage():
    print("usage: ./computor.py [-f | --fast] EQUATION")


def getargs():
    fast = False
    eq = sys.argv[1]
    if len(sys.argv) > 2:
        if sys.argv[1] == "-f" or sys.argv[1] == "--fast":
            fast = True
            eq = sys.argv[2]
        else:
            if sys.argv[2] == "-f" or sys.argv[2] == "--fast":
                fast = True
            eq = sys.argv[1]
    return eq, fast


def main():
    if not len(sys.argv) >= 2:
        usage()
        sys.exit(1)
    eq, fast = getargs()
    print("Input: " + eq)
    eq = sanitize(eq)
    if not eq:
        sys.exit(1)
    coef = parse.coefficients(eq)
    d = degree(coef)
    if not edge_case(coef, d):
        sys.exit(1)
    red = reduced(coef)
    if red[0] == "-":
        coef = parse.coefficients(sanitize("0 = " + red.split("=")[0].strip()))
        red = reduced(coef)
    # print(eq)
    print(f"Reduced form: {red}")
    if not validpoly(red):
        sys.exit(1)
    d = degree(coef)
    print(f"Polynomial degree: {d}")
    sys.exit(solver.solve(d, coef, fast))


if __name__ == "__main__":
    main()
