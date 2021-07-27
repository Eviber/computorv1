#!/usr/bin/env python3

from random import randint

def r():
    return (randint(-5000, 5000)/100)

def randompoly():
    a = r()
    b = r()
    c = r()
    s = f"{a}X^2 " + (f"- {-b}" if (b < 0) else f"+ {b}") + "X "
    s = s + (f"- {-c}" if (c < 0) else f"+ {c}")
    return (s)

def main():
    print(randompoly() + " = " + randompoly())

if __name__ == "__main__":
    main()
