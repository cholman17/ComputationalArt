""" Randomly Generated Computational Art -- Christina Holman. I added 2 functions called squared and cubed """

from random import *
from math import *
import random
from PIL import Image

title = raw_input('Title your piece: ')
num_frames = input('How many frames? ')
def build_random_function(min_depth, max_depth):
	basic = ['x','y']
	func = ['x','y','cos_pi','sin_pi','prod','squared', 'cubed','avg']	
	
    	if max_depth == 0: #If max depth = zero, function ends
        	index = random.randint(0,2)
   	elif min_depth <= 0: #min depth <= zero, function ends
       		index = random.randint(0,8)
	if max_depth == 1:
        	return basic[random.randint(0,1)]
   	else:
        	block = func[random.randint(2,6)]
        	if block == 'prod' or 'avg': #when block requires 2 inputs
            		return [block, build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]
       		elif not block == 'prod':
           		return [block, build_random_function(min_depth-1, max_depth-1)] 	


def evaluate_random_function(f, x, y, t):
#checks if f equals any of these operations
	if f[0] == 'x':
		return x
	elif f[0] == 'y':
		return y
	elif f[0] == 'squared':
		return evaluate_random_function(f[1],x,y,t)**2
	elif f[0] == 'avg':
		return (evaluate_random_function(f[1],x,y,t)+evaluate_random_function(f[2],x,y))/2
	elif f[0] == 'cos_pi':
		return cos(pi*evaluate_random_function(f[1],x,y,t))
	elif f[0] == 'sin_pi':
		return sin(pi*evaluate_random_function(f[1],x,y,t))
	elif f[0] == 'cubed':
		return evaluate_random_function(f[1],x,y,t)**3.
	elif f[0] == 'prod':
		return evaluate_random_function(f[1],x,y,t)*evaluate_random_function(f[2],x,y,t)
	else:
		return t


def remap_interval(val,input_interval_start,input_interval_end, output_interval_start, output_interval_end):
	valf = float(val-input_interval_start)/(input_interval_end-input_interval_start)
	valw = valf*(output_interval_end-output_interval_start)+output_interval_start
	return valw

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.
        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]
        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, num_frames, x_size=350, y_size=350):
	""" Generate computational art and save as an image file.
	filename: string filename for image (should be .png)
	x_size, y_size: optional args to set image dimensions (default: 350)
	"""
	# Functions for red, green, and blue channels - where the magic happens!
	red_function = build_random_function(5, 9)
	green_function = build_random_function(6, 9)
	blue_function = build_random_function(7, 13)

   	# Create image and loop over all pixels
	for k in range(num_frames):
	    	im = Image.new("RGB", (x_size, y_size))
	    	pixels = im.load()
		t = remap_interval(k, 0, num_frames-1, -1, 1)
	    	for i in range(x_size):
			for j in range(y_size):
		    		x = remap_interval(i, 0, x_size, -1, 1)
		    		y = remap_interval(j, 0, y_size, -1, 1)
		    		pixels[i, j] = (
		            		color_map(evaluate_random_function(red_function, x, y, t)),
		            		color_map(evaluate_random_function(green_function, x, y, t)),
		            		color_map(evaluate_random_function(blue_function, x, y, t))
		            )

    	im.save(filename+'_'+str(k)+'.png')

if __name__ == '__main__':
	import doctest
	doctest.testmod()
    	# Create some computational art!
	print '++++++++++'+str(title)+'+++++++++++'
	for i in range(num_frames):
		generate_art('frame_%s'%i, 100)
