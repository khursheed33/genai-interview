"""Solution: recursive segment match (*, one; #, rest-or-all)."""


def match(pattern, key):
    pp, kp = pattern.split("."), key.split(".")

    def go(pi, ki):
        if pi == len(pp):
            return ki == len(kp)
        if pp[pi] == "#":
            return any(go(pi + 1, j) for j in range(ki, len(kp) + 1))
        return ki < len(kp) and (pp[pi] == "*" or pp[pi] == kp[ki]) and go(pi + 1, ki + 1)

    return go(0, 0)
