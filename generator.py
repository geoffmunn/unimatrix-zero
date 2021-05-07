#!/usr/bin/env python

import os
import argparse
from unimatrix_zero import zero

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('max_number', help = 'Maximum number in this wheel', type = int)
    parser.add_argument('line_length', help = 'Length of each line in this wheel', type = int)
    parser.add_argument('picked', help = 'How many numbers are picked?', type = int)
    parser.add_argument('cover', help = 'How many numbers in each line do you want covered?', type = int)
    parser.add_argument('testmode', help = 'Run this as a test only', nargs = '?', const = False, type = bool)
    args = parser.parse_args()

    max_number 	= args.max_number
    line_length = args.line_length
    picked 		= args.picked
    cover 		= args.cover
    testmode 	= args.testmode

    if testmode is None:
        testmode = False

    file_name	= "Combo " + str(max_number) + " " + str(line_length) + " " + str(picked) + " " + str(cover) + ".txt"
    path 		= './results/' + file_name

    if os.path.isfile(path) and testmode != True:
        print ("Combo already exists, exiting")
        exit()

    results = zero.create(max_number, line_length, picked, cover, testmode, path)

    if testmode == True:
        print (results)
        print ("Total lines: " + str(len(results)))
        print ("Test mode - no file was updated")
    else:
        print ("Total lines: " + str(len(results)))
        print ("Written to file " + file_name)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()