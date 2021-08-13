#!/usr/bin/env python3

import sys

def debug(*s):
    print(*s)

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

from decimal import Decimal
import decimal

def parsenum(n):
    val = 1
    if not '𝓍' in n:
        c = 0
        val = Decimal(n)
    else:
        if n[0] == '-' and n[1] == '𝓍':
            val = Decimal('-1')
        elif n[0] != '𝓍':
            val = Decimal(n.split("𝓍")[0])
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
                    red = "-" if c != 0 else "-1"
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
            print("𝓍 = 𝓍\nThis equation is always true.")
        else:
            print(reduced(coef) + "\nThis equation has no solution.")
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
    eq = list(filter(None, eq.replace(" ", "").replace('X', '𝓍').replace('x', '𝓍').replace("-", "+-").replace("=", "+=+").strip("+").split("+")))
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

def hasdecimals(n):
    return (n != n.to_integral_value())

def frac(n1, n2):
    n1 = Decimal(n1)
    n2 = Decimal(n2)
    while hasdecimals(n1) or hasdecimals(n2):
        n1 = (n1 * 10).normalize()
        n2 = (n2 * 10).normalize()
    sign = -1 if ((n1 < 0) ^ (n2 < 0)) else 1
    n1 = n1 if n1 >= 0 else -n1
    n2 = n2 if n2 >= 0 else -n2
    if n1 % n2 == 0:
        return (sign * n1/n2, Decimal(1))
    g = gcd(n1,n2)

    n1 = n1 // g
    n2 = n2 // g
    if n2 < 0:
        n1 = -n1
        n2 = -n2
    return (sign * n1,n2)

def remove_exponent(d):
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()

def fracstr(n1, n2):
    (n1, n2) = frac(n1, n2)
    n1 = remove_exponent(n1)
    n2 = remove_exponent(n2)
    if n2 == 1:
        return (f"{n1:g}")
    f = f"{n1}/{n2}"
    n = str(remove_exponent(n1/n2))
    if len(f) >= len(n):
        return (n)
    return (f)

def addfactor(res, n):
    if not n in res.keys():
        res[n] = 1
    else:
        res[n] = res[n] + 1

def primefactors(n):
    res = {}
    if (hasdecimals(n)):
        return ({n: 1})
    while n % 2 == 0:
      addfactor(res, 2)
      n = n / 2
    for i in range(3,int(approx_sqrt(n))+1,2):
        while (n % i == 0):
            addfactor(res, i)
            n = n / i
            if n == 1:
                return(res)
    if n > 2:
        addfactor(res, int(n))
    return(res)

def approx_sqrt(n):
    s = n
    while (s != (s+(n/s))/2):
        s = (s+(n/s))/2
    return (s)

#𝓍𝒾√
def sqrt(n):
    imaginary = ''
    if (n < 0):
        n = -n
        imaginary = '𝒾'
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

def solve1(coef):
    print("The solution is:")
    if not 0 in coef.keys() or coef[0] == 0:
        print("𝓍 = 0")
    else:
        print("𝓍 = " + fracstr(-coef[0], coef[1]))

def simplifyFrac(a, b, n, sq):
    a1, a2 = frac(-b, 2*a)
    b1, b2 = frac(n, 2*a)
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
    return remove_exponent(n.quantize(Decimal("0.000001")))

def getapprox(a, b, delta):
    if delta >= 0:
        a1 = (-b-approx_sqrt(delta))/(2*a)
        a2 = (-b+approx_sqrt(delta))/(2*a)
        if (hasdecimals(a1) and len(str(remove_exponent(a1)).split('.')[1]) > 6) or fast:
            a1 = f" ≈ {dround(a1)}"
        else:
            a1 = ""
        if (hasdecimals(a2) and len(str(remove_exponent(a2)).split('.')[1]) > 6) or fast:
            a2 = f" ≈ {dround(a2)}"
        else:
            a2 = ""
        return (a1, a2)
    else:
        realpart = f"{dround((-b)/(2*a))}"
        tmp = dround(approx_sqrt(-delta)/(2*a))
        if tmp == 1:
            tmp = ''
        if realpart != "0":
            a1 = a2 = realpart
            if tmp != 0:
                a1 = a1 + f" - {tmp}𝒾"
                a2 = a2 + f" + {tmp}𝒾"
        else:
            a1, a2 = f"-{tmp}𝒾", f"{tmp}𝒾"
    if ((delta < 0 and ('.' in a1 or '/' in a1)) or delta >= 0 and (hasdecimals(a1) and len(str(remove_exponent(a1)).split('.')[1])) > 6) or fast:
        a1 = f" ≈ {a1}"
    else:
        a1 = ""
    if ((delta < 0 and ('.' in a2 or '/' in a2)) or delta >= 0 and (hasdecimals(a2) and len(str(remove_exponent(a2)).split('.')[1])) > 6) or fast:
        a2 = f" ≈ {a2}"
    else:
        a2 = ""
    return (a1, a2)

def solve2nonzero(a, b, delta):
    approx1, approx2 = getapprox(a, b, delta)
    if fast:
        print("𝓍1" + approx1)
        print("𝓍2" + approx2)
        return
    n, sq = sqrt(delta)
    if sq == "":
        print("𝓍1 = " + fracstr(-b-n, 2*a) + approx1)
        print("𝓍2 = " + fracstr(-b+n, 2*a) + approx2)
    else:
        dividend, divisor, sq = simplifyFrac(a, b, n, sq)
        tmp = ''
        if divisor != 1 and dividend != 0:
            tmp = fracstr(dividend, divisor)
            if not '.' in tmp and not '/' in tmp:
                dividend = tmp
            else:
                dividend = f"({dividend}"
                sq = f"{sq})"
        elif dividend != 0:
            dividend = f"{dividend} "
            sq = f" {sq}"
        if divisor != 1:
            if dividend == tmp:
                divisor = f"/{divisor}"
                dividend = f"{dividend} "
                sq = f" {sq}"
            else:
                divisor = f" / {divisor}"
        else:
            divisor = ''
        if dividend == 0:
            print(f"𝓍1 = -{sq}{divisor}{approx1}\n𝓍2 =  {sq}{divisor}{approx2}")
        else:
            print(f"𝓍1 = {dividend}-{sq}{divisor}{approx1}\n𝓍2 = {dividend}+{sq}{divisor}{approx2}")

def solve2(coef):
    a = 0 if not 2 in coef.keys() else coef[2]
    b = 0 if not 1 in coef.keys() else coef[1]
    c = 0 if not 0 in coef.keys() else coef[0]
    delta = b*b-4*a*c
    print(f"a = {fracstr(a, 1)} ; b = {fracstr(b,1)}  ; c = {fracstr(c, 1)}")
    print(f"delta = {fracstr(delta, 1)}")
    if delta == 0:
        print("Discriminant is zero, the solution is:\n𝓍 = " + fracstr(-b, 2*a))
    elif delta < 0:
        print("Discriminant is strictly negative, the two solutions are:") #𝒾
        solve2nonzero(a,b,delta)
    else:
        print("Discriminant is strictly positive, the two solutions are:")
        solve2nonzero(a,b,delta)
def usage():
    print("usage: ./computor.py [-f | --fast] EQUATION")

def main():
    global fast
    fast = False
    if not len(sys.argv) >= 2:
        usage()
        return
    eq = sys.argv[1]
    if (sys.argv[1][0] == '-' and len(sys.argv) > 2):
        if (sys.argv[1] == "-f" or sys.argv[1] == "--fast"):
            fast = True
        eq = sys.argv[2]
    print(eq)
    eq = sanitize(eq)
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
        try:
            solve2(coef)
        except decimal.InvalidOperation:
                print("Error: values too extremes")
    elif d > 2:
        print(f"The polynomial degree is stricly greater than 2, I can't solve.")

if __name__ == "__main__":
    main()
