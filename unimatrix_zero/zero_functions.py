#!/usr/bin/env python

from math import comb

def sequence_number(cur_line, max_number):
    '''
    This will return the sequence number for the provided combination (CSN)
    It is a port of a script found here: https://saliu.com/combination.html

    Parameters:
        cur_line	(list):	This is the combination to get the CSN for. Must be in ascending order.
        max_number 	(int):	The maximum possible number in the entire range

    Returns:
        csn 		(int): The sequence number for the combination
    '''

    line_length = len(cur_line)
    cur_total 	= 0
    csn 		= 0
    max_index 	= line_length - 1

    cur_vals 	= [0] * max_index

    for i in range(max_index):

        cur_vals[i] = 0

        if i != 0:
            cur_vals[i] = cur_vals[i - 1]

        while True:
            cur_vals[i] = cur_vals[i] + 1

            nCr = comb(max_number - cur_vals[i], line_length - i - 1)

            cur_total = cur_total + nCr

            if cur_vals[i] >= cur_line[i]:
                break

        cur_total = cur_total - nCr

    csn = cur_total + cur_line[line_length - 1] - cur_line[max_index - 1]

    return csn

def next_combination(cur_line, max_number):
    '''
    Get the next value of the provided combination
    NOTE: for speed purposes, we are using DESCENDING array values

    Parameters:
        cur_line 	(list):	This is the combination to get the next value for.
        max_number	(int):	The maximum possible number in the entire range

    Returns:
        cur_line 	(list): A single list item
    '''

    # Add 1 to the [0] indice.
    # If this new value exceeds the max value, then move down the list and add one until it's ok

    if(cur_line[0] + 1 <= max_number):
        cur_line[0] += 1
    else:
        index = 1
        while index < len(cur_line):
            if cur_line[index] + 1 > max_number - index:
                index += 1
            else:
                break

        if index < len(cur_line):
            cur_line[index] += 1
        else:
            return False

        for i in reversed(range(index)):
            cur_line[i] = cur_line[i + 1] + 1

    return cur_line

def new_template(length):
    '''
    Set up a basic list with numbers in reverse order

    Parameters:
        length 		(int): 	The length of the list

    Returns:
        cur_subset 	(list): A single list item
    '''

    cur_subset = []
    for j in range(length, 0, -1):
        cur_subset.append(j - 1)

    return cur_subset

def covered_subsets_template(picked, cover):
    '''
    Create a template of the subsets of size $cover from $picked

    Parameters:
        picked 	(int):	The picked numbers in the wheel conditions
        cover 	(int):	How many numbers are covered at least once by $picked numbers

    Returns:
        results	(list):	A nested list of lines of $cover
    '''

    # Build up the template for covered subsets of the picked numbers

    results = []
    cur_subset = new_template(cover)

    while cur_subset != False:
        val = cur_subset[:]
        val.sort()
        results.append(val)
        cur_subset = next_combination(cur_subset, picked - 1)

    return results

def covered_subsets_length_template(line_length, cover):
    '''
    Build up the template for covered subsets of the length numbers

    Parameters:
        line_length (int): 	The length of the line - how many numbers in a line
        cover		(int): 	How many numbers are covered at least once by $picked numbers

    Returns:
        results 	(list): A nested list of lines of length $cover
    '''

    results = []
    cur_subset = new_template(cover)

    while cur_subset != False:
        val = cur_subset[:]
        val.sort()
        results.append(val)
        cur_subset = next_combination(cur_subset, line_length - 1)

    return results

def missing_length_template(max_number, line_length, picked, cover):
    '''
    Create the template of the missing combinations for the $line_length numbers
    We need special accomodations for when picked is less than or equal to the line length or cover

    Parameters:
        max_number 	(int): 	The maximum possible number in the entire range
        line_length	(int): 	The length of the line - how many numbers in a line
        picked 		(int): 	The picked numbers in the wheel conditions
        cover 		(int): 	How many numbers are covered at least once by $picked numbers

    Returns:
        results 	(list): A nested list of lines of $line_length
    '''

    results = []

    if line_length > cover:
        cur_subset = new_template(line_length - cover)
        if picked > line_length:
            if picked > cover:
                while cur_subset != False:
                    val = cur_subset[:]
                    val.sort()
                    results.append(val)
                    cur_subset = next_combination(cur_subset, max_number - cover - 1) 	#-1 is required for 8, 6, 7, 4

            else:
                missing_length_template = [[]]
        else:
            while cur_subset != False:
                val = cur_subset[:]
                val.sort()
                results.append(val)
                cur_subset = next_combination(cur_subset, max_number - cover - 1)

    else:
        results = [[]]

    return results

def missing_picked_cover_template(max_number, line_length, picked, cover):
    '''
    Create the template of missing combinations between $cover and $picked

    Parameters:
        max_number 	(int): 	The maximum possible number in the entire range
        line_length	(int): 	The length of the line - how many numbers in a line
        picked 		(int): 	The picked numbers in the wheel conditions
        cover 		(int): 	How many numbers are covered at least once by $picked numbers

    Returns:
        results 	(list):	A nested list of lines of length $picked - $cover
    '''

    results = []

    if picked > line_length:
        cur_subset = new_template(picked - cover)
        while cur_subset != False:
            val = cur_subset[:]
            val.sort()
            results.append(val)
            cur_subset = next_combination(cur_subset, max_number - cover - 1)

    else:
        if picked > cover:
            cur_subset = new_template(picked - cover)
            while cur_subset != False:
                val = cur_subset[:]
                val.sort()
                results.append(val)
                cur_subset = next_combination(cur_subset, max_number - cover - 1)

        else:
            results = [[]]

    return results
