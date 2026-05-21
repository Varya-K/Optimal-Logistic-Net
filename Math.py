eps = 1e-5

def Bg(a, b):
    return a - b > eps

def Sm(a, b):
    return b - a > eps

def Eq(a, b):
    return abs(a - b) < eps