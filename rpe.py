# rpe.py - a solver for polynomial equations

import gmpy2 as gmpy
import sys

# ------------------------------------------------------------------------------

def to_float(x):
    # return float(x)
    # use high-precision floating-point numbers
    return gmpy.mpfr(x, 300)

# ------------------------------------------------------------------------------

def eval_func(p, r):
    # Evaluate polynomial equation with coefficients in list 'p' (p(x)) at x=r
    fx = to_float("0.0")
    for e in p:
        fx *= r
        fx += to_float(e)
    return fx

# ------------------------------------------------------------------------------

def create_init_vector(a):
    # Convert a_0, a_1, ... a_n to w_0, w_1, ... w_n-1
    w = [0.0] * (len(a)-1)
    for i in range(len(a)-1):
        w[i] = (-1.0 * to_float(a[i+1])) / (to_float(a[0]))
    return w

# ------------------------------------------------------------------------------

def F(w):
    # Compute the degree of the polynomial equation.
    N = len(w)

    # Result list containing values Fn(0,1,2,3, ...)
    F_n = []

    # F_n[0..N-2] = 0.0
    for i in range(N-1):
        F_n.append(to_float("0.0"))

    # F_n[N-1] = 1.0
    F_n.append(to_float("1.0"))

    # Compute successive values of the Fn derived recursive function.
    n = N
    while True:
        z = to_float("0.0")
        for i in range(N):
            z += w[i] * F_n[n-i-1]
        F_n.append(z)
        yield z
        n += 1
 
# ------------------------------------------------------------------------------
 
def reduce(a, x):
    # Remove root "x".
    b = []
    b.append("%.6f"%(to_float(a[0])))
    for i in range(1,len(a)-1,1):
        b.append(to_float(a[i]) + to_float(b[i-1])*x)
        b[i] = "%.6f"%(b[i])
    return b
 
# ------------------------------------------------------------------------------
 
#
# Solve x*x*x - 6*x*x + 11*x - 6 = 0, that is (x - 1)*(x - 2)*(x - 3) = 0
#
 
print("")
print("Solving equation:")
print("    x*x*x - 6*x*x + 11*x - 6 = 0")
print("    Refactored as (x - 1)*(x - 2)*(x - 3) = 0")
print("    Which roots are 1, 2, 3.")
print("")
 
# 1 * x*x*x - 6*x*x + 11*x - 6
a = ["1.0", "-6.0", "11.0", "-6.0"]
 
while True:
    w = create_init_vector(a)
    f = F(w)
    F_n1 = next(f)
    n = 0
    while True:
        n += 1
        F_n2 = next(f)
        x = F_n2/F_n1
        y = eval_func(a, x)
        if abs(y) < to_float("0.000000000000000000000000000000000000000001"):
            print("")
            print(a)
            print("")
            print("    n =", n)
            print("")
            print("    Fn(n  ) =", F_n2)
            print("    Fn(n-1) =", F_n1)
            print("")
            print("    x =", x)
            print("--> x = %.6f"%(x))
            print("")
            print("    f(x) =", y)
            print("    f(x) = %.6f"%(y))
            print("")
            a = reduce(a, x)
            if len(a) == 1:
                sys.exit(1)
            break
        F_n1 = F_n2
 
# ------------------------------------------------------------------------------
 
# <Program output>
#
# Solving equation:
#     x*x*x - 6*x*x + 11*x - 6 = 0
#     Refactored as (x - 1)*(x - 2)*(x-3) = 0
#     Which roots are 1, 2, 3.
#
#
# ['1.0', '-6.0', '11.0', '-6.0']
#
#     n = 92
#
#     Fn(n  ) = 1.0604475735226644e+45
#     Fn(n-1) = 3.5348252450755478e+44
#
#     x = 3.0
# --> x = 3.000000
#
#     f(x) = 0.0
#     f(x) = 0.000000
#
#
# ['1.000000', '-3.000000', '2.000000']
#
#     n = 51
#
#     Fn(n  ) = 9007199254740990.0
#     Fn(n-1) = 4503599627370495.0
#
#     x = 2.0
# --> x = 2.000000
#
#     f(x) = 0.0
#     f(x) = 0.000000
#
#
# ['1.000000', '-1.000000']
#
#     n = 1
#
#     Fn(n  ) = 1.0
#     Fn(n-1) = 1.0
#
#     x = 1.0
# --> x = 1.000000
#
#     f(x) = 0.0
#     f(x) = 0.000000
