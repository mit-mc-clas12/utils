"""
Basic implementation of a priority system for
assigning users an instant priority.

Each user is assigned a static priority, this
is an integer.  When the system works properly
the ratio of jobs between users can be computed
as the ratio of their priorities.

weight = priority / total_running_jobs 

"""

from copy import deepcopy

def weight_time_sort(items_, weights_, times_):
    """ A version of insertion sort modified to 
    do a sort based on weight but break ties
    with times. Algorithm is O(n**2) time complex
    but our user base is so small, it doesn't matter.

    Inputs: 
    -------
    - items - some items that you want sorted according to 
    the weights given and times given (list)
    - weights - list of weights between 0, 1
    - times - unix times 

    Returns:
    --------
    sorted list of items

    """

    assert(len(weights_) == len(times_))
    assert(len(weights_) == len(items_))

    items = deepcopy(items_)
    weights = deepcopy(weights_)
    times = deepcopy(times_)

    out_items = []
    out_weights = []
    out_times = []
    while items:

        big_index = 0 
        for index, (i,w,t) in enumerate(zip(items, weights, times)):
            if w > weights[big_index]:
                big_index = index
            elif w == weights[big_index]:
                if t < times[big_index]:
                    big_index = index

        out_items.append(items.pop(big_index))
        out_weights.append(weights.pop(big_index))
        out_times.append(times.pop(big_index))
        
    return out_items, out_weights, out_times
