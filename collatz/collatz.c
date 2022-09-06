//The collatz conjecture

#include <cs50.h>
#include <stdio.h>

int collatz( int n);

int main(void)
{
    int number = get_int("Select a number: ");
    int times = collatz(number);
    printf("iterated %i times until reached 1\n", times);
}

int collatz( int n)
{
    if (n == 1)
        return 0;
    else if (n % 2 == 0)
        return 1 + collatz(n / 2);
    else
        return 1 + collatz(3*n + 1);
}

//sexy code