#!/usr/bin/env python

import os
import argparse
from math import comb
from unimatrix_zero import zero_functions

def get_best(picked, cover, max_number, lines):

    subset = zero_functions.new_template(picked, False)

    hits 		= {}
    best_subset	= {}
    best_count	= {}
    line_count	= {}
    coverage	= {}
    nCr			= 0

    for i in range(2, cover + 1):
        best_subset[i]	= []
        best_count[i]	= 0
        line_count[i]	= 0
        coverage[i]		= set()

    while subset != False:
        nCr += 1
        # Take this subset and check to see if it's found in the list

        for i in range(2, cover + 1):
            line_count[i] = 0

        ordered_subset = subset[:]
        ordered_subset.sort()

        for line in lines:

            hit_count = 0
            for number in subset:
                if number in line:
                    hit_count += 1

            for i in range(2, cover + 1):
                if hit_count >= i:
                    line_count[i] 	+= 1
                    coverage[i].add(zero_functions.sequence_number(ordered_subset, max_number))

        for i in range(2, cover + 1):
            if line_count[i] >= best_count[i]:
                if line_count[i] > best_count[i]:
                    best_subset[i]	= []
                    best_count[i]	= line_count[i]

                best_subset[i].append(ordered_subset[:])

        subset = zero_functions.next_combination(subset, max_number)

    return best_subset, best_count, coverage, nCr

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('max_number', help = 'Maximum number in this wheel', type = int)
    parser.add_argument('line_length', help = 'Length of each line in this wheel', type = int)
    parser.add_argument('picked', help = 'How many numbers are picked?', type = int)
    parser.add_argument('cover', help = 'How many numbers in each line do you want covered?', type = int)

    args = parser.parse_args()

    max_number 	= args.max_number
    line_length = args.line_length
    picked 		= args.picked
    cover 		= args.cover

    version = str('1.0')

    file_name	= "Wheel " + str(max_number) + " " + str(line_length) + " " + str(picked) + " " + str(cover) + ".txt"
    path 		= './results/' + file_name

    if os.path.isfile(path) == False:
        print ("Wheel file does not exist, exiting")
        exit()

    file = open(path, 'r', newline='\n')

    lines	= []
    read	= False
    valid	= False
    newfile	= []

    while True:
        # Get next line from file
        line = file.readline()

        if len(line) >= 5 and line[0:5] == '*****':
            if read == True:
                read = False
            else:
                read = True

        if read == True:
            if line[0:5] != '*****':
                if line != '':
                    bit2 = list(map(int, line.split(': ')[1].replace("\n", '').split(' ')))
                    lines.append(bit2)

        newfile.append(line)

        if len(line) > 11 and line[0:11] == 'Time taken:':
            valid = True
            break

        if not line:
            break

    file.close()

    if valid == False:
        print ('This wheel does not seem to be complete - please rebuild it')
        exit()

    hits_col = len(str(line_length) + ' if ' + str(line_length) + ' ')
    hits_text = ('Hits' + (' ' * hits_col))[0:hits_col]

    tested_col  = len(str(comb(max_number, line_length)))
    if tested_col < len('Tested'):
        tested_col = len('Tested')
    tested_text = ('Tested' + (' ' * tested_col))[0:tested_col]

    covered_col  = len(str(comb(max_number, line_length)))
    if covered_col < len('Covered'):
        covered_col = len('Covered')
    covered_text = ('Covered' + (' ' * covered_col))[0:covered_col]

    header_text = hits_text + ' | ' + tested_text + ' | ' + covered_text + ' | Percent | Most hits |'
    horizontal_bar = '-' * len(header_text)
    print (header_text)
    print (horizontal_bar)

    newfile.append('\n*****\nCoverage report (version: ' + version + ')\n\n')
    newfile.append(header_text + '\n')
    newfile.append(horizontal_bar + '\n')

    for j in range (2, picked + 1):

        best_subset, best_count, hits, nCr = get_best(j, cover, max_number, lines)

        for i in range(2, j + 1):
            if i <= cover:
                hits_val = str(i) + ' if ' + str(j)
                if len(hits_val) < len(hits_text):
                     hits_val = (hits_val + (' ' * hits_col))[0:hits_col]

                tested_val = str(nCr)
                if len(tested_val) < len(tested_text):
                    tested_val = (tested_val + (' ' * tested_col))[0:tested_col]

                covered_val = str(len(hits[i]))
                if len(covered_val) < len(covered_text):
                    covered_val = (covered_val + (' ' * covered_col))[0:covered_col]

                precent_val = str('{:.2f}'.format(len(hits[i])/nCr*100) + '       ')[0:7]

                best_val = (str(best_count[i]) + '         ')[0:9]

                report_line = hits_val + ' | ' + tested_val + ' | '+ covered_val + ' | ' + precent_val + ' | ' + best_val  + ' |'
                print (report_line)
                newfile.append(report_line + '\n')

    print (horizontal_bar)
    newfile.append(horizontal_bar)

    file = open(path,'w')
    file.writelines(newfile)
    file.close()

if __name__ == "__main__":

    """ This is executed when run from the command line """
    main()