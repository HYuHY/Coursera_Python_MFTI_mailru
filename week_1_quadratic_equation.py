"""
решает квадратное уравнение с действительными корнями
"""
import sys

try:
    coef = [int(sys.argv[x]) for x in range(1,4)]
    D = coef[1]**2 - 4 * coef[0] * coef[2]
    print (coef, "Discriminant: ",D)
    if D < 0: raise ValueError
except ValueError:
    print("Сoefficients must be integer and discriminant is positive")



x1 = (- coef[1] + D**(1/2)) / 2 * coef[0]
x2 = (- coef[1] - D**(1/2)) / 2 * coef[0]
if x1 - int(x1) != 0 :
    print("Root x1 not integer: ", x1) 
else:
    print("Root x1: ", int(x1)) 
if x2 - int(x2) != 0 :
    print("Root x2 not integer: ", x2)
else:
    print("Root x2: ", int(x2))




