#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, string argv[])
{
    //get key and make sure is a valid key, otherwise complain. Also get key as int.
    int key;
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        for (int i = 0, k = 0; argv[1][i] > 0; i++)
        {
            if (isdigit(argv[1][i]) == false)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        key = atoi(argv[1]);
    }
    //get plain text
    string plaintext = get_string("Plaintext: ");

    //encipher and print
    printf("Ciphertext: ");
    for (int i = 0, c = 0; i < strlen(plaintext); i++)
        if (isalpha(plaintext[i]))
        {
            if (isupper(plaintext[i]))
            {
                c = ((plaintext[i] + key) - 65) % 26;
                int offset = c - (plaintext[i] - 65);
                printf("%c", plaintext[i] + offset);
            }
            else
            {
                c = ((plaintext[i] + key) - 97) % 26;
                int offset = c - (plaintext[i] - 97);
                printf("%c", plaintext[i] + offset);
            }
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    printf("\n");
}

