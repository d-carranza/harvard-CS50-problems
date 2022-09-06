#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Prompt the user to enter an integer between 1 and 8
    //If height is an integer between 1 and 8 continue, if not prompt again
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);


    //Start a for a higher level loop for scan through the rows and add 1 to i at the end
    for (int i = 1; i <= h; i++)
    {
        // And a various for loop to print the columns of each program

        // 1.space columns print h-i spaces
        for (int j = 1; j <= (h - i); j++)
        {
            printf(" ");
        }
        // # 2.columns print i #
        for (int k = 1; k <= i; k++)
        {
            printf("#");
        }
        // 3.print "  "
        printf("  ");
        // # 4.columns print i #
        for (int l = 1; l <= i; l++)
        {
            printf("#");
        }
        printf("\n");
    }
}