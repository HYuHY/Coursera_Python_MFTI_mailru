"""
считает сумму цифр в составе числа, подаваемого через параметр командной строки
"""
import sys

digit_sum = 0
try:
    insert_digit = sys.argv[1]
    for dig in insert_digit:
        digit_sum += int(dig)
    print("sum = ", digit_sum)
except ValueError:
    print("Please enter digits only")
