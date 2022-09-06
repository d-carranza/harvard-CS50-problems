from cs50 import get_float

while True:
    change = get_float("Change owed: ")
    if change > 0:
        break

coins = [0.25,0.1,0.05,0.01]
n = 0

for i in range(4):
    while round(change, 2) >= coins[i]:
        change -= coins[i]
        n += 1

print("{}".format(n))