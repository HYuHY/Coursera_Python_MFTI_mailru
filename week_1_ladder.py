"""
рисует лесенку из # по числу-параметру в командной строке
"""
import sys

try:
    stair_number = int(sys.argv[1])
    for tier in range(1, stair_number+1):
        tier_str = " " * (stair_number - tier) + "#" * tier
        print(tier_str)
except ValueError:
    print("Please enter digits as number of stairs")
