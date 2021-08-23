#!/usr/bin/env python3

from random import randint


def r(d=0):
    d = pow(10, d)
    return randint(-5 * d, 5 * d) / 1 * d


def randompoly():
    a = r()
    b = r()
    c = r()
    s = f"{a:g}X^2 " + (f"- {-b:g}" if (b < 0) else f"+ {b:g}") + "X "
    s = s + (f"- {-c:g}" if (c < 0) else f"+ {c:g}")
    return s


def main():
    print(randompoly() + " = " + randompoly())


if __name__ == "__main__":
    main()
