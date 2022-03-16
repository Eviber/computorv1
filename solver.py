from mathtools import *
import decimal


def getapprox(a, b, delta):
    if delta >= 0:
        a1 = (-b - approx_sqrt(delta)) / (2 * a)
        a2 = (-b + approx_sqrt(delta)) / (2 * a)
        if (
            hasdecimals(a1) and len(str(remove_exponent(a1)).split(".")[1]) > 6
        ) or fast:
            a1 = f" ≈ {dround(a1)}"
        else:
            a1 = ""
        if (
            hasdecimals(a2) and len(str(remove_exponent(a2)).split(".")[1]) > 6
        ) or fast:
            a2 = f" ≈ {dround(a2)}"
        else:
            a2 = ""
        return (a1, a2)
    else:
        realpart = f"{dround((-b)/(2*a))}"
        tmp = dround(approx_sqrt(-delta) / (2 * a))
        if tmp == 1:
            tmp = ""
        if realpart != "0":
            a1 = a2 = realpart
            if tmp != 0:
                a1 = a1 + f" - {tmp}𝒾"
                a2 = a2 + f" + {tmp}𝒾"
        else:
            a1, a2 = f"-{tmp}𝒾", f"{tmp}𝒾"
    if (
        (delta < 0 and ("." in a1 or "/" in a1))
        or delta >= 0
        and (hasdecimals(a1) and len(str(remove_exponent(a1)).split(".")[1])) > 6
    ) or fast:
        a1 = f" ≈ {a1}"
    else:
        a1 = ""
    if (
        (delta < 0 and ("." in a2 or "/" in a2))
        or delta >= 0
        and (hasdecimals(a2) and len(str(remove_exponent(a2)).split(".")[1])) > 6
    ) or fast:
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
        print("𝓍1 = " + fracstr(-b - n, 2 * a) + approx1)
        print("𝓍2 = " + fracstr(-b + n, 2 * a) + approx2)
    else:
        dividend, divisor, sq = simplifyFrac(a, b, n, sq)
        tmp = ""
        if divisor != 1 and dividend != 0:
            tmp = fracstr(dividend, divisor)
            if "." not in tmp and "/" not in tmp:
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
            divisor = ""
        if dividend == 0:
            print(f"𝓍1 = -{sq}{divisor}{approx1}")
            print(f"𝓍2 =  {sq}{divisor}{approx2}")
        else:
            print(f"𝓍1 = {dividend}-{sq}{divisor}{approx1}")
            print(f"𝓍2 = {dividend}+{sq}{divisor}{approx2}")


def solve2(coef):
    a = 0 if 2 not in coef.keys() else coef[2]
    b = 0 if 1 not in coef.keys() else coef[1]
    c = 0 if 0 not in coef.keys() else coef[0]
    delta = b * b - 4 * a * c
    print(f"a = {fracstr(a, 1)} ; b = {fracstr(b,1)}  ; c = {fracstr(c, 1)}")
    print(f"delta = {fracstr(delta, 1)}")
    if delta == 0:
        print("Discriminant is zero, the solution is:\n𝓍 = " + fracstr(-b, 2 * a))
    elif delta < 0:
        print("Discriminant is strictly negative, the two solutions are:")  # 𝒾
        solve2nonzero(a, b, delta)
    else:
        print("Discriminant is strictly positive, the two solutions are:")
        solve2nonzero(a, b, delta)


def solve1(coef):
    print("The solution is:")
    if 0 not in coef.keys() or coef[0] == 0:
        print("𝓍 = 0")
    else:
        print("𝓍 = " + fracstr(-coef[0], coef[1]))


def solve(d, coef, f):
    global fast
    fast = f
    if d == 1:
        solve1(coef)
    elif d == 2:
        try:
            solve2(coef)
        except decimal.InvalidOperation:
            print("Error: values too extremes")
    elif d > 2:
        print(f"The polynomial degree is stricly greater than 2, I can't solve.")
