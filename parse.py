from decimal import Decimal
import mathtools


def parsenum(n):
    val = 1
    if "X" not in n:
        c = 0
        val = Decimal(n)
    else:
        if n[0] == "-" and n[1] == "X":
            val = Decimal("-1")
        elif n[0] != "X":
            val = Decimal(n.split("X")[0])
        if "^" not in n:
            c = 1
        else:
            c = Decimal(n[n.index("^") + 1:])
    return (val, c)


def coefficients(eq):
    coef = {}
    right = False
    for n in eq:
        if "=" not in n:
            val = 1
            exp = 0
            for part in n.split("*"):
                (v, c) = parsenum(part)
                val = v * val
                exp = c + exp
            if right:
                val = -val
            if exp in coef.keys():
                coef[exp] = mathtools.remove_exponent(coef[exp] + val)
                if coef[exp] == 0:
                    del coef[exp]
            else:
                coef[exp] = mathtools.remove_exponent(val)
        else:
            right = True
    return coef
