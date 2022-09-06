#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define BLOCK_SIZE 512

typedef uint8_t BYTE;

int jpeg(BYTE buffer[])
{
    if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
    {
        return 1;
    }
    return 0;
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    FILE *raw_file = fopen(argv[1], "r");
    if (raw_file == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    BYTE buffer[BLOCK_SIZE];
    FILE *img;
    int counter = 0;
    char *filename = malloc(8 * sizeof(BYTE));

    while (fread(buffer, 1, BLOCK_SIZE, raw_file) == BLOCK_SIZE)
    {
        if (jpeg(buffer) == 1)
        {
            if (counter != 0)
            {
                fclose(img);
            }
            sprintf(filename, "%03i.jpg", counter++);
            img = fopen(filename, "w");
            fwrite(buffer, 1, BLOCK_SIZE, img);
        }
        else if (counter > 0)
        {
            fwrite(buffer, 1, BLOCK_SIZE, img);
        }
    }
    free(filename);
    fclose(img);
    fclose(raw_file);
}