// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 187751;

// Hash table
unsigned int hash(const char *word);
node *table[N];
int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    for (node *tmp = table[hash(word)]; tmp != NULL; tmp = tmp->next)
    {
        if (strcasecmp(tmp->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int hash = 0;
    for (int i = 0; i <= strlen(word); i++)
    {
        hash = (31 * hash + toupper(word[i])) % N;
    }
    return hash;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }
    char *word = malloc(LENGTH + 1);
    if (word == NULL)
    {
        return false;
    }
    while (fscanf(dict, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        int place = hash(word);
        strcpy(n->word, word);
        if (table[place] == NULL)
        {
            n->next = NULL;
        }
        else
        {
            n->next = table[place];
        }
        table[place] = n;
        word_count++;
    }
    fclose(dict);
    free(word);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i <= N; i++)
    {
        while (table[i] != NULL)
        {
            node *tmp = table[i]->next;
            free(table[i]);
            table[i] = tmp;
        }
    }
    return true;
}