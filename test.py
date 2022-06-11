import os
os.system("cls")
ltest = list(range(1, 20))
print(ltest)


def ftransform(x):
    if x % 3 == 0:
        return f"{x} mul of 3"
    else:
        return ''


lCalc = list(map(ftransform, ltest))
print(lCalc)

# -------------------------

map(lambda num: num ** 2, numbers)

print("---")
print("END")
print("---")
