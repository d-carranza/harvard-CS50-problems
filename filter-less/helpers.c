#include "helpers.h"
#include <math.h>
// Convert image to grayscale (average of r g and b values)
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //Loop to find each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            //Find the average and replace the values
            float average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia (algorithm)
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    //Loop to find each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Apply the algorithm
            int sepia_red = round((.393 * image[i][j].rgbtRed) + (.769 * image[i][j].rgbtGreen) + (.189 * image[i][j].rgbtBlue));
            int sepia_green = round((.349 * image[i][j].rgbtRed) + (.686 * image[i][j].rgbtGreen) + (.168 * image[i][j].rgbtBlue));
            int sepia_blue = round((.272 * image[i][j].rgbtRed) + (.534 * image[i][j].rgbtGreen) + (.131 * image[i][j].rgbtBlue));
            if (sepia_red > 255)
            {
                sepia_red = 255;
            }
            if (sepia_green > 255)
            {
                sepia_green = 255;
            }
            if (sepia_blue > 255)
            {
                sepia_blue = 255;
            }
            image[i][j].rgbtRed = sepia_red;
            image[i][j].rgbtGreen = sepia_green;
            image[i][j].rgbtBlue = sepia_blue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{



    //Loop to find each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            //Change the width of the pixel with (width - X)
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][(width - 1) - j];
            image[i][(width - 1) - j] = tmp;
        }
    }
    return;
}

// Blur image (average the 9 pixels 3x3 around)
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //create copy
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image [i][j];
        }
    }
    //Loop to find each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = 0;
            int green = 0;
            int blue = 0;
            float counter = 0.0;
            for (signed int a = -1; a <= 1; a++)
            {
                for (signed int b = -1; b <= 1; b++)
                {
                    //die skip pixels outside of height and width
                    if (((i + a) < 0) || ((j + b) < 0) || ((i + a) >= height) || ((j + b) >= width))
                    {
                        continue;
                    }
                    //calculate sum of colours
                    red = red + copy[i + a][j + b].rgbtRed;
                    green = green + copy[i + a][j + b].rgbtGreen;
                    blue = blue + copy[i + a][j + b].rgbtBlue;
                    counter++;
                }
            }
            //sum
            image[i][j].rgbtRed = round(red / counter);
            image[i][j].rgbtGreen = round(green / counter);
            image[i][j].rgbtBlue = round(blue / counter);
        }
    }
    return;
}
