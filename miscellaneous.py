from typing import List
#find minimum function for finding the the minimum distance in cursors
def find_minimum(xdata: List,ydata: List, cmpr_x: float, cmpr_y: float) -> int:
    if len(xdata) == 0:
        return None
    minimum = cmpr_x**2 + cmpr_y**2#set a baseline minimum
    min_i = 0
    for i in range(len(xdata)):
        distance = (cmpr_x - xdata[i])**2 + (cmpr_y - ydata[i])**2
        if distance < minimum:
            minimum = distance
            min_i = i
    return min_i#returns the index that this happens at not the value
