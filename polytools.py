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
    return red


def degree(coef):
    if len(coef) > 0:
        return max(k for k, v in coef.items())
    return 0


def edge_case(coef, d):
    if d == 0:
        if 0 not in coef.keys() or coef[0] == 0:
            print("𝓍 = 𝓍\nThis equation is always true.")
        else:
            print(reduced(coef) + "\nThis equation has no solution.")
        return False
    return True
