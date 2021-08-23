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
    if sys.argv[1][0] == "-" and len(sys.argv) > 2:
        if sys.argv[1] == "-f" or sys.argv[1] == "--fast":
            fast = True
        eq = sys.argv[2]
    return eq, fast


def main():
    if not len(sys.argv) >= 2:
        usage()
        return
    eq, fast = getargs()
    print(eq)
    eq = sanitize(eq)
    if not eq:
        return
    coef = parse.coefficients(eq)
    d = degree(coef)
    if not edge_case(coef, d):
        return
    red = reduced(coef)
    if red[0] == "-":
        coef = parse.coefficients(sanitize("0 = " + red.split("=")[0].strip()))
        red = reduced(coef)
    # print(eq)
    print(f"Reduced form: {red}")
    d = degree(coef)
    print(f"Polynomial degree: {d}")
    solver.solve(d, coef, fast)


if __name__ == "__main__":
    main()
