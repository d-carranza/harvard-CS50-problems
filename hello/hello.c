#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string user = get_string("What's your name? ");
    printf("hello %s\n", user);
}