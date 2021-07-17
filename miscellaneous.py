from typing import List
import os
#find minimum function for finding the the minimum distance in cursors
def find_minimum(xdata: List,ydata: List, cmpr_x: float, cmpr_y: float) -> int:
    '''returns the index of x and y value that has the lowest distance from the cmpr_x
    and cmpr_y values'''
    if len(xdata) == 0:
        return None
    minimum = cmpr_x**2 + cmpr_y**2#set a baseline minimum
    min_i = 0
    for i in range(len(xdata)):
        distance = (cmpr_x - xdata[i])**2 + (cmpr_y - ydata[i])**2
        if distance < minimum:
            minimum = distance
            min_i = i
    return min_i#returns the index corresponding to the minimum not the value

#avoid overwriting data
def available_name(filename: str) -> str:
    '''checks if the filename is available and returns the next best name'''
    exists = os.path.exists(filename)

    depth =  0

    while exists:
        dot = filename.find('.')
        if dot == -1:#if there is no dot do this
            if depth == 0:
                filename = filename + ' (1)'

            else:
                filename = filename[:-2] + str(depth + 1) + ')'
        else:#If there is a dot do this
            if depth == 0:
                filename = filename[:dot] + '(' + str(depth + 1) + ')' + filename[dot:] #add the brackets and number before the dot
            else:
                filename = filename[:dot - 2] + str(depth + 1) + filename[dot - 1:]#replace the number

        exists = os.path.exists(filename)
        depth += 1

    return filename
