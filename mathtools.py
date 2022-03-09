# Decimal is a special type that is better suited for base 10 numbers
from decimal import Decimal
import re


def gcd(n1, n2):
    if n1 < n2:
        (n1, n2) = (n2, n1)
    if n1 % n2 == 0:
        return n2
    return gcd(n2, n1 % n2)


def hasdecimals(n):
    return '.' in '{0:f}'.format(remove_exponent(n))
    #return n != n.to_integral_value()


def frac(n1, n2):
    n1 = Decimal(n1)
    n2 = Decimal(n2)
    while hasdecimals(n1) or hasdecimals(n2):
        n1 = (n1 * 10)
        n2 = (n2 * 10)
    sign = -1 if ((n1 < 0) ^ (n2 < 0)) else 1
    n1 = n1 if n1 >= 0 else -n1
    n2 = n2 if n2 >= 0 else -n2
    if n1 % n2 == 0:
        return (sign * n1 / n2, Decimal(1))
    g = gcd(n1, n2)

    n1 = n1 // g
    n2 = n2 // g
    if n2 < 0:
        n1 = -n1
        n2 = -n2
    return (sign * n1, n2)


def remove_exponent(d):
    s = '{0:f}'.format(d)
    if '.' in s:
        if Decimal(s.split('.')[1]) == 0:
            s = s.split('.')[0]
        else:
            s = re.sub(r"(\d+\.\d*?)0+$", r"\1", s)
    return Decimal(s)
    #return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


def fracstr(n1, n2):
    (n1, n2) = frac(n1, n2)
    n1 = remove_exponent(n1)
    n2 = remove_exponent(n2)
    if n2 == 1:
        return f"{n1:g}"
    f = f"{n1}/{n2}"
    n = '{0:f}'.format(remove_exponent(n1 / n2))
    if len(f) >= len(n):
        return n
    return f


def addfactor(res, n):
    if n not in res.keys():
        res[n] = 1
    else:
        res[n] = res[n] + 1


def primefactors(n):
    res = {}
    if hasdecimals(n):
        return {n: 1}
    while n % 2 == 0:
        addfactor(res, 2)
        n = n / 2
    for i in range(3, int(approx_sqrt(n)) + 1, 2):
        while n % i == 0:
            addfactor(res, i)
            n = n / i
            if n == 1:
                return res
    if n > 2:
        addfactor(res, int(n))
    return res


def approx_sqrt(n):
    s = n
    while s != (s + (n / s)) / 2:
        s = (s + (n / s)) / 2
    return s


def sqrt(n):
    imaginary = ""
    if n < 0:
        n = -n
        imaginary = "𝒾"
    multiple = 1
    square = 1
    factors = primefactors(n)
    for f in factors.keys():
        while factors[f] >= 2:
            multiple = multiple * f
            factors[f] = factors[f] - 2
        if factors[f] == 1:
            square = square * f
    if square == 1:
        return (multiple, imaginary)
    return (multiple, imaginary + f"√{square}")


def simplifyFrac(a, b, n, sq):
    a1, a2 = frac(-b, 2 * a)
    b1, b2 = frac(n, 2 * a)
    if a2 < b2:
        a1 = a1 * b2 / a2
        a2 = a2 * b2 / a2
    elif a2 > b2:
        f = fracstr(b1 * a2, b2)
        b1 = b1 * a2 / b2
        b2 = b2 * a2 / b2
    if b1 != 1:
        if not hasdecimals(b1) or len(f) > len(f"{b1:g}"):
            sq = f"{b1:g}{sq}"
        else:
            sq = f"({f}){sq}"
    return (remove_exponent(a1), remove_exponent(b2), sq)


def dround(n):
    s = '{0:f}'.format(n)
    if '.' in s:
        parts = s.split('.')
        n = Decimal(parts[0] + '.' + parts[1][:6])
        tmp = "0." + parts[1][6:]
        if Decimal(tmp) >= 0.5:
            n = n + Decimal("0.000001")
    return remove_exponent(n)
    #return remove_exponent(n.quantize(Decimal("0.000001")))
