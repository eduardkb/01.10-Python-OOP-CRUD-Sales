import os
from unittest import load_tests
from resources.ekbMod import clear_scren
clear_scren()


def ftransform(x):
    if x % 3 == 0:
        return f"{x} mul of 3"
    else:
        return ''


ltest = list(range(1, 20))
print(f"original list: {ltest}")
lCalc = list(map(ftransform, ltest))
print(f"transformed list: {lCalc}")

# -------------------------
print("---")

numbers = list(range(1, 20))
print(f"original list: {numbers}")
transNum = list(map(lambda num: num ** 2, numbers))
print(f"transformed list: {transNum}")

print("---")
print("END")
print("---")
