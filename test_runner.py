#!/usr/bin/env python

import argparse
from unimatrix_zero import zero

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('test_case', help = 'Run a particular test case', type = str)
    args = parser.parse_args()

    test_case = args.test_case

    if test_case == 'test1':
        max_number 	= 10
        line_length	= 6
        picked 		= 6
        cover 		= 5
        line_count	= 15
    elif test_case == 'test2':
        max_number 	= 10
        line_length	= 6
        picked 		= 6
        cover 		= 4
        line_count	= 3
    elif test_case == 'test3':
        max_number 	= 10
        line_length	= 6
        picked 		= 7
        cover 		= 5
        line_count  = 4
    elif test_case == 'test4':
        max_number 	= 10
        line_length	= 6
        picked 		= 7
        cover 		= 4
        line_count  = 2
    elif test_case == 'test5':
        max_number 	= 10
        line_length	= 6
        picked 		= 5
        cover 		= 5
        line_count	= 59
    elif test_case == 'test6':
        max_number 	= 10
        line_length	= 6
        picked 		= 4
        cover 		= 4
        line_count	= 23
    elif test_case == 'test7':
        max_number 	= 10
        line_length	= 6
        picked 		= 5
        cover 		= 4
        line_count 	= 8
    elif test_case == 'test8':
        max_number 	= 10
        line_length	= 6
        picked 		= 4
        cover 		= 3
        line_count	= 4
    elif test_case == 'test9':
        max_number 	= 10
        line_length	= 3
        picked 		= 6
        cover 		= 3
        line_count	= 12
    elif test_case == 'test10':
        max_number	= 10
        line_length = 3
        picked		= 5
        cover		= 2
        line_count  = 3

    results = zero.create(max_number, line_length, picked, cover, True, "")

    if len(results) == line_count:
        print ("Test successful: line count is correct")
    else:
        if len(results) > line_count:
            print ("Test FAILED: more lines than expected")
            print ("Run this command to see the results:")
            print ("python generator.py",max_number,line_length,picked,cover,"-mode=test")
        else:
            print ("Test FAILED: fewer lines than expected")
            print ("Run this command to see the results:")
            print ("python generator.py",max_number,line_length,picked,cover,"-mode=test")

if __name__ == "__main__":
    main()