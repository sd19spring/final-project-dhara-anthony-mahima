"""
set_up.py generates computational art for each of the four moods. It builds off
of the Computational Art Mini Project done in Software Design at Olin College.
The number of images created has been hard coded to 20 images, but that can be
altered. The more images you have the better your moving background will look.
However, set_up.py already takes about 15 minutes to run when generating 20 images.

If you are not satisfied with one of the folders of art, you can adjust the ranges of
color in the fuction range_finder and specify which folder you want to change by
getting rid of the outer for loop in the main function so that all folders are not
changed.
"""

#import these libraries
import random
import math
from PIL import Image


def build_random_function(min_depth, max_depth):
    """Build a random function.

    Builds a random function of depth at least min_depth and depth at most
    max_depth. (See the assignment write-up for the definition of depth
    in this context)

    Args:
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function

    Returns:
        The randomly generated function represented as a nested list.
        (See the assignment writ-eup for details on the representation of
        these functions)

    """
    #Establish empty list to build off of.
    function = []
    #There were lots of problems with min_depth decreasing too far. 1 should be the minimum.
    if min_depth < 1:
        min_depth = 1
    #Determine depth of the function. Only really used to determine if base case is triggered.
    from random import randint
    depth = randint(min_depth, max_depth)
    #Base case that ends recursion. All functions with depth = 1 must be either "x" or "y" or "t"
    if depth == 1:
        generator = randint(1, 3)
        if generator == 1:
            function.append("x")
        if generator == 2:
            function.append("y")
        if generator == 3:
            function.append("t")
        return function
    else:
    #A random integer generator determines which of the 6 functions will be used.
        generator = randint(1, 6)
    #The "prod" and "avg" functions have 2 inputs and therefore 2 more lists have to be appended.
        if generator == 1:
            function.append("prod")
            #Max_depth and min_depth have to decrease by 1 for each recursion.
            function.append(build_random_function(min_depth - 1, max_depth - 1))
            function.append(build_random_function(min_depth - 1, max_depth - 1))
            return function
        if generator == 2:
            function.append("avg")
            function.append(build_random_function(min_depth - 1, max_depth - 1))
            function.append(build_random_function(min_depth - 1, max_depth - 1))
            return function
        if generator == 3:
            function.append("sin_pi")
            function.append(build_random_function(min_depth - 1, max_depth - 1))
            return function
        if generator == 4:
            function.append("cos_pi")
            function.append(build_random_function(min_depth - 1, max_depth - 1))
            return function
        if generator == 5:
            function.append("square")
            function.append(build_random_function(min_depth - 1, max_depth - 1))
            return function
        if generator == 6:
            function.append("root_abs")
            function.append(build_random_function(min_depth - 1, max_depth - 1))
            return function


def evaluate_random_function(f, x, y, t):
    """Evaluate the random function f with inputs x,y,t.

    The representation of the function f is defined in the assignment write-up.

    Args:
        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        t: the value of t to be used to evaluate the function

    Returns:
        The function value
    """
    #The first term of the function list determines which function is called, therefore, conditionals are used.
    if f[0] == "prod":
        return evaluate_random_function(f[1], x, y, t) * evaluate_random_function(f[2], x, y, t)
    if f[0] == "avg":
        return 0.5 * (evaluate_random_function(f[1], x, y, t) + evaluate_random_function(f[2], x, y, t))
    if f[0] == "cos_pi":
    #Cos_pi and sin_pi were having problems returning numbers in scientific notation that were very very close to 0.
    #Therefore, I implemented this conditional which returns 0 when cos_pi or sin_pi are within 0.01 of 0.
        if math.cos(math.pi * evaluate_random_function(f[1], x, y, t)) < 0.01 and math.cos(math.pi * evaluate_random_function(f[1], x, y, t)) > -0.01:
            return 0
        else:
            return math.cos(math.pi * evaluate_random_function(f[1], x, y, t))
    if f[0] == "sin_pi":
        if math.sin(math.pi * evaluate_random_function(f[1], x, y, t)) < 0.01 and math.sin(math.pi * evaluate_random_function(f[1], x, y, t)) > -0.01:
            return 0
        else:
            return math.sin(math.pi * evaluate_random_function(f[1], x, y, t))
    if f[0] == "square":
        return evaluate_random_function(f[1], x, y, t)**2
    if f[0] == "root_abs":
    #You cannot take the square root of the negative, so I had to take the square root of the absolute value.
        return abs(evaluate_random_function(f[1], x, y, t))**0.5
    if f[0] == "x":
        return x
    if f[0] == "y":
        return y
    if f[0] == "t":
        return t


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """Remap a value from one interval to another.

    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].

    Args:
        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values

    Returns:
        The value remapped from the input to the output interval
    """
    # TODO: implement this
    valfraction = (val - input_interval_start) / (input_interval_end - input_interval_start)
    outputfraction = valfraction * (output_interval_end - output_interval_start)
    remap = outputfraction + output_interval_start
    return remap


def color_map(val, min_rgb=0, max_rgb=255):
    """Maps input value between -1 and 1 to an integer 0-255, suitable for use as an RGB color code.

    Args:
        val: value to remap, must be a float in the interval [-1, 1]

    Returns:
        An integer in the interval [0,255]
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, min_rgb, max_rgb)
    return int(color_code)

def range_finder(mood=['negative', 'low energy']):
    ranges = {'red_min':0,'red_max':0,
                'green_min':0,'green_max':0,
                'blue_min':0,'blue_max':0}

    if mood == ['negative', 'low energy']:
        ranges['red_min'] = 0
        ranges['red_max'] = 100
        ranges['blue_min'] = 50
        ranges['blue_max'] = 150
        ranges['green_min'] = 100
        ranges['green_max'] = 175
    if mood == ['positive', 'low energy']:
        ranges['red_min'] = 100
        ranges['red_max'] = 200
        ranges['blue_min'] = 0
        ranges['blue_max'] = 100
        ranges['green_min'] = 50
        ranges['green_max'] = 150
    if mood == ['negative', 'high energy']:
        ranges['red_min'] = 90
        ranges['red_max'] = 150
        ranges['blue_min'] = 100
        ranges['blue_max'] = 200
        ranges['green_min'] = 50
        ranges['green_max'] = 70
    if mood == ['positive', 'high energy']:
        ranges['red_min'] = 150
        ranges['red_max'] = 255
        ranges['blue_min'] = 100
        ranges['blue_max'] = 255
        ranges['green_min'] = 60
        ranges['green_max'] = 255

    return ranges
def new_functions():
    '''
    Returns the new functions for red,green, and blue using build random
    '''
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    return red_function,green_function,blue_function

def generate_art(ranges, t, red_function, green_function, blue_function, x_size=427, y_size=240):
    """Generate computational art and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    red_min = ranges['red_min']
    red_max = ranges['red_max']
    blue_min = ranges['blue_min']
    blue_max = ranges['blue_max']
    green_min = ranges['green_min']
    green_max = ranges['green_max']

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                color_map(evaluate_random_function(red_function, x, y, t), min_rgb=red_min, max_rgb=red_max),
                color_map(evaluate_random_function(green_function, x, y, t), min_rgb=green_min, max_rgb=green_max),
                color_map(evaluate_random_function(blue_function, x, y, t), min_rgb=blue_min, max_rgb=blue_max)
            )
    return im

def main():
    '''
    Creates folders for every mood category and calls helper functions to generate 20
    images for each folder
    '''
    moods = [['positive', 'low energy'],
            ['negative', 'low energy'],
            ['positive', 'high energy'],
            ['negative', 'high energy']]
    for mood in moods:
        red_function, green_function, blue_function = new_functions()
        for i in range(20):
            time = remap_interval(i,0,20,-1,1)
            location = 'images/'+ mood[0]+'_'+mood[1] +'/' +str(i) + '.png'
            ranges = range_finder(mood)
            im = generate_art(ranges,time,red_function, green_function, blue_function)
            im.save(location)


if __name__ == '__main__':
    main()
