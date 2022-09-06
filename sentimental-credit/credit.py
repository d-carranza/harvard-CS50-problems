from cs50 import get_int

while True:
    cardnumber = get_int("Number: ")
    n = cardnumber
    if (n * 2) % 2 == 0:
        break
sum = 0
m = 0

for i in range(1, n):

    if i % 2 == 0:
        m = 2 * (n % 10)

        for j in range(int(m)):
            sum += m % 10
            m = (m - m % 10) / 10
    else:
        sum += n % 10
        n = (n - n % 10) / 10

if sum % 10 == 0:
    if cardnumber / 10000000000000 == 34 or cardnumber / 10000000000000 == 37:
        print("AMEX")

    elif cardnumber / 100000000000000 > 50 and cardnumber / 100000000000000 < 56:
        print("MASTERCARD")

    elif cardnumber / 1000000000000 == 4 or cardnumber / 1000000000000000 == 4:
        print("VISA")

    else:
        print("INVALID")

else:
    print("INVALID")
