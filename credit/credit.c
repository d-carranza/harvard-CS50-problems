#include <cs50.h>
#include <stdio.h>


int main(void)
{
    long cardnumber;
    long n;
    //prompts the user for a credit card number with DO While
    do
    {
        cardnumber = get_long("Your credit card number: ");
        n = cardnumber;
    }
    while ((n * 2) % 2 != 0);

    //checksum algorithm
    long m;
    long sum = 0;
    //loop to take number by number from the end
    for (int i = 1; n > 0; i++)
    {
        //if even multiply number by 2 and loop that number to add everything
        //(then add to checksum and go to the next number)
        if (i % 2 == 0)
        {
            m = 2 * (n % 10);
            for (int j = 1; m > 0; j++)
            {
                sum += m % 10;
                m = (m - m % 10) / 10;
            }
        }
        //if odd just add to sum
        else
        {
            sum += n % 10;
        }
        n = (n - n % 10) / 10;
    }


//invalid if doesn't satisfy the algorithm
    if (sum % 10 == 0)
    {
        //here comes the sorting
        //1. if removing 13 digits que remaining number is 34 or 37 AMEX
        if (cardnumber / 10000000000000 == 34 || cardnumber / 10000000000000 == 37)
        {
            printf("AMEX\n");
        }
        //2. if removing 14 digits que remaining number is 51,52,53,54,55 MASTERCARD
        else if (cardnumber / 100000000000000 > 50 && cardnumber / 100000000000000 < 56)
        {
            printf("MASTERCARD\n");
        }
        //3. if removing 12 or 15 digits que remaining number is 4 VISA
        else if (cardnumber / 1000000000000 == 4 || cardnumber / 1000000000000000 == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}