import ekbMod
ekbMod.clear_screen()

dict = {"Nome": "Eduard", "aGE": 33, "num": 4}


lKeys = list(dict.keys())
print(lKeys)
lKeys = [x.lower() for x in lKeys]
print(lKeys)

# reading key
# print(dict["Nome"])
# print(dict["Age".lower()])
