from cs50 import get_int

while True:
    n = get_int("Height: ")
    if n > 0 and n < 9:
        break

for i in range(1, n + 1):
    print(" " * (n-i) + "#" * i)
