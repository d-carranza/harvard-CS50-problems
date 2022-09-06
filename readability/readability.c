#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    //promp string
    string text = get_string("Text: ");

    //declare variables
    int length = strcspn(text, "\0");
    float letters = 0;
    float words = 1;
    float sentences = 0;
    float l;
    float s;
    float index;

    //get letters
    for (int i = 0; i < length; i++)
    {
        if (((text[i] >= 65) && (text[i] <= 90)) || ((text[i] >= 97) && (text[i] <= 122)))
        {
            letters += 1;
        }
    }

    //get words
    for (int i = 0; i < length; i++)
    {
        if (text[i] == 32)
        {
            words += 1;
        }
    }

    //get sentences
    for (int i = 0; i < length; i++)
    {
        if (text[i] == 46 || text[i] == 33 || text[i] == 63)
        {
            sentences += 1;
        }
    }

    //apply formula
    l = letters * 100 / words;
    s = sentences * 100 / words;
    index = (0.0588 * l - 0.296 * s - 15.8) + 0.5;

    //print result
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) index);
    }
}