#!/usr/bin/env python

import time
import os
import copy
from math import comb
from unimatrix_zero import zero_functions

def convert(seconds):
    status 				= ''
    seconds 			= round(seconds, 2)
    minutes, seconds 	= divmod(seconds, 60)
    hours, minutes 		= divmod(minutes, 60)

    periods 	= [('hours', hours), ('minutes', minutes), ('seconds', seconds)]
    time_string = ', '.join('{} {}'.format(value, name)
                            for name, value in periods
                            if value)

    result = '{} {}'.format(status, time_string).strip()

    if result == '':
        result = '0.01 seconds'

    return result

def next_line(covered_subsets_template: list, covered_subsets_length_template: list, missing_picked_cover_template: list, missing_length_template: list, covered_picked_csns: list, cur_line: list, max_number: int, bottom_index: int):

    # Reset the maximum statistics because we're starting a new line search
    candidate_results: list = {}

    # Step 2: Go through each subset of $cur_line. These are of size $covered from $picked
    # $covered cannot be larger than $line_length (or $picked)
    for subset in covered_subsets_template:
        
        # Map each number in $cur_line to a spot in the subset template
        templated_subset: list = []
        for j in subset:
            templated_subset.append(cur_line[j])

        # Find the missing numbers from this subset
        missing_subset_numbers: list = []
        for j in range(1, max_number + 1):
            if j not in templated_subset:
                missing_subset_numbers.append(j)

        # So now we have the missing numbers for the actual subset of the current line
        # Together they should add up to $line_length

        # Step 3: Now combine them to lines of length $line_length - these are potential nominated lines
        for missing_length_subset in missing_length_template:

            # This full line is a candidate for what can cover the current line
            candidate_line = templated_subset[:]
            for j in missing_length_subset:
                candidate_line.append(missing_subset_numbers[j])
            candidate_line.sort()

            current_csns: list = []
            
            # Step 4: Go through each covered subset (length = line_length) in the candidate line
            for covered_subset in covered_subsets_length_template:

                # Map each spot in the subset to a $candidate_line number
                templated_covered_subset: list = []
                for j in covered_subset:
                    templated_covered_subset.append(candidate_line[j])

                templated_covered_subset.sort()

                # Find the missing numbers from this subset
                missing_candidate_subset_numbers: list = []
                for j in range(1, max_number + 1):
                    if j not in templated_covered_subset:
                        missing_candidate_subset_numbers.append(j)

                # Step 5: Now build this up to $picked
                for missing_picked_cover_subset in missing_picked_cover_template:

                    # Add the missing numbers onto the templated line:
                    covered_picked_line: list = templated_covered_subset[:]
                    for j in missing_picked_cover_subset:
                        covered_picked_line.append(missing_candidate_subset_numbers[j])

                    covered_picked_line.sort()

                    # This full line is a candidate for what can cover $cur_line
                    # Get the CSN so we can check if we've already got it:
                    csn: int = zero_functions.sequence_number(covered_picked_line, max_number)

                    # If the CSN is below the bottom-most index, then we can assume it's covered
                    # This should be a bit quicker for very large wheels
                    if csn >= bottom_index:
                        if csn not in covered_picked_csns:
                            current_csns.append(csn)
            
            differences = sorted(list(set(current_csns).difference(set(covered_picked_csns))))
            
            candidate_results[' '.join([str(item) for item in candidate_line])] = differences
    
    return candidate_results

def scan(covered_subsets_template: list, covered_subsets_length_template: list, missing_picked_cover_template: list, missing_length_template: list, covered_picked_csns: list, cur_line: list, max_number: int, bottom_index: int):

    # Reset the maximum statistics because we're starting a new line search
    max_coverage_count: int	 = 0
    max_candidate_line: list = []
    max_current_csns: list	 = []

    # Step 2: Go through each subset of $cur_line. These are of size $covered from $picked
    # $covered cannot be larger than $line_length (or $picked)
    for subset in covered_subsets_template:
        # Map each number in $cur_line to a spot in the subset template
        templated_subset:list = []
        for j in subset:
            templated_subset.append(cur_line[j])

        # Find the missing numbers from this subset
        missing_subset_numbers:list = []
        for j in range(1, max_number + 1):
            if j not in templated_subset:
                missing_subset_numbers.append(j)

        # So now we have the missing numbers for the actual subset of the current line
        # Together they should add up to $line_length

        # Step 3: Now combine them to lines of length $line_length - these are potential nominated lines
        #quick_exit: bool = False
        for missing_length_subset in missing_length_template:

            # This full line is a candidate for what can cover the current line
            candidate_line: list = templated_subset[:]
            for j in missing_length_subset:
                candidate_line.append(missing_subset_numbers[j])
            candidate_line.sort()

            # Reset the coverage statistics:
            coverage_count: int	= 0
            current_csns: list 	= []

            # Step 4: Go through each covered subset (length = line_length) in the candidate line
            for covered_subset in covered_subsets_length_template:

                # Map each spot in the subset to a $candidate_line number
                templated_covered_subset: list = []
                for j in covered_subset:
                    templated_covered_subset.append(candidate_line[j])
                templated_covered_subset.sort()

                # Find the missing numbers from this subset
                missing_candidate_subset_numbers = []
                for j in range(1, max_number + 1):
                    if j not in templated_covered_subset:
                        missing_candidate_subset_numbers.append(j)

                # Step 5: Now build this up to $picked
                for missing_picked_cover_subset in missing_picked_cover_template:

                    # Add the missing numbers onto the templated line:
                    covered_picked_line = templated_covered_subset[:]
                    for j in missing_picked_cover_subset:
                        covered_picked_line.append(missing_candidate_subset_numbers[j])

                    covered_picked_line.sort()

                    # This full line is a candidate for what can cover $cur_line
                    # Get the CSN so we can check if we've already got it:
                    csn = zero_functions.sequence_number(covered_picked_line, max_number)

                    # If the CSN is below the bottom-most index, then we can assume it's covered
                    # This should be a bit quicker for very large wheels
                    if csn > bottom_index:
                        if csn not in covered_picked_csns:
                            current_csns.append(csn)
                    
            # The coverage is the total number of CSNs that aren't in the $covered_picked_csns list
            differences: list 	= list(set(current_csns).difference(set(covered_picked_csns)))
            coverage_count: int = len(differences)

            # If this is the current best result, then keep a copy of it:
            if coverage_count > max_coverage_count:
                max_coverage_count: int	 = coverage_count
                max_candidate_line: list = candidate_line
                max_current_csns: list 	 = current_csns
    
    return max_coverage_count, max_candidate_line, max_current_csns
        
def create(max_number: int, line_length: int, picked: int, cover: int, testmode: bool, path: str):

    version: str	  = '1.4.0'
    start_time: float = time.time()
    bottom_index: int = 1

    # Dirty workaround alert! I'm not sure how to properly fix this.
    # In the cases of 8 2 2 2, bottom_index needs to be zero
    if picked >= line_length:
       bottom_index = 0

    covered_subsets_template		= zero_functions.covered_subsets_template(picked, cover)
    covered_subsets_length_template	= zero_functions.covered_subsets_length_template(line_length, cover)
    missing_length_template			= zero_functions.missing_length_template(max_number, line_length, picked, cover)
    missing_picked_cover_template	= zero_functions.missing_picked_cover_template(max_number, line_length, picked, cover)

    covered_picked_csns: list = []		# This is the canonical list of picked lines we have covered
    final_lines: dict		  = {}		# This is the list of lines we will return with
    lines_from_picked: int    = comb(max_number, picked)

    # Now start generating some lines!
    if testmode == False:
        f = open(path + '.progress', "w")
        f.write("Unimatrix Zero\nVersion: " + version + "\n\nRange:       " + str(max_number) + "\nLine length: " + str(line_length) + "\nPicked:      " + str(picked) + "\nCover:       " + str(cover) + "\n\n*****\n")
        f.close()

    # Create the first line:
    cur_line:list = []
    for j in range(picked, 0, -1):
        cur_line.append(j)

    coverage_total: int = 0

    mode: str = '>='

    # Step 1: Take the next line of $picked length
    for i in range(1, lines_from_picked + 1):
        print ('*********')
        print ('NEW LOOP')
        print ('*********')
        print (i, cur_line)

        #test1 = [1, 2, 3, 4]
        #test2 = [3, 4, 5, 6]

        #print ('union:', list(set(test1).union(set(test2))))
        #print ('differences:', list(set(test1).difference(set(test2))))
        #exit()

        # Do not process this line if it's already covered
        if i >= bottom_index and i not in covered_picked_csns:

            # get the best pair.
            # To do this, we need every uncovered candidate, and their coverage:
            first_line = next_line(covered_subsets_template, covered_subsets_length_template, missing_picked_cover_template, missing_length_template, covered_picked_csns, cur_line, max_number, bottom_index)
            
            # A running total of the coverage of the pair combination so far
            combined_coverage_count = -1
            
            # The lines we've currently picked as being our candidates
            candidate_lines = {}

            # the CSNs that the candidate lines cover
            combined_csns = []

            for line in first_line:

                print ('**************************')
                print ('we want to simulate', line, ' which covers ',len(first_line[line]),' CSNs:', first_line[line])

                # Now we need to find the next line available
                cur_line2 = copy.copy(cur_line)

                # This is a combination of all the CSNs from the current line in $first_line, and anything we've definitely covered so far
                temp_covered_picked_csns1 = list(set(first_line[line]).union(set(covered_picked_csns)))

                # Quit here if this one line covers everything
                if len(temp_covered_picked_csns1) == lines_from_picked:
                    print ('TOTAL COVERAGE FOUND!')
                    candidate_lines = {}
                    combined_csns = temp_covered_picked_csns1
                    candidate_lines[line] = str('{:.2f}'.format(((coverage_total + len(first_line[line]))/lines_from_picked) * 100)) + '%'

                    print ('new candidate:')
                    print ('line 1:', line, '(',len(first_line[line]),')')
                    print ('covered CSNs:', combined_csns)
        
                    break
    
                else:
                    
                    # Otherwise, go through every line from here and find the first one that's not covered
                    for j in range(i + 1, lines_from_picked + 1):

                        # Get the next line for this combination
                        cur_line2 = zero_functions.next_combination(cur_line2, max_number)    
                
                        # If this is not covered in the CSNs from the first line (+already covered CSNs):
                        if j >= bottom_index and j not in temp_covered_picked_csns1:
                            
                            max_coverage_count, max_candidate_line, max_current_csns = scan(covered_subsets_template, covered_subsets_length_template, missing_picked_cover_template, missing_length_template, temp_covered_picked_csns1, cur_line2, max_number, bottom_index)

                            temp_covered_picked_csns2 = list(set(max_current_csns).union(set(temp_covered_picked_csns1)))

                            if len(temp_covered_picked_csns2) > combined_coverage_count:
                                print ('new candidate:')
                                print ('line 1:', line, '(',len(first_line[line]),')')
                                print ('line 2:', max_candidate_line, '(',max_coverage_count,')')

                                combined_coverage_count = len(temp_covered_picked_csns2)
                                print ('new combined coverage count:', combined_coverage_count)
                                print ('csns:', len(temp_covered_picked_csns2), temp_covered_picked_csns2)

                                candidate_lines = {}
                                candidate_lines[line] = str('{:.2f}'.format((len(temp_covered_picked_csns1)/lines_from_picked) * 100)) + '%'
                                candidate_lines[' '.join([str(item) for item in max_candidate_line])] = str('{:.2f}'.format((len(temp_covered_picked_csns2)/lines_from_picked) * 100)) + '%'

                                combined_csns = temp_covered_picked_csns2
            
            # Update the list of covered CSNs
            for csn in combined_csns:
                if csn >= bottom_index:
                    if csn not in covered_picked_csns:
                        covered_picked_csns.append(csn)
            
            print ('the best combo is:', candidate_lines)
            print ('this combo covers:', combined_csns, '(', len(combined_csns), ')')
            print ('total covered csns:', covered_picked_csns, len(covered_picked_csns))
            print (((coverage_total + len(first_line[line])) / lines_from_picked) * 100, mode)

            if testmode == False:
                f = open(path + '.progress', "a")
                count: int = 1
                for final_line in candidate_lines: 
                    f.write(str(len(final_lines) + count) + ' (' + candidate_lines[final_line] + ') ' + final_line + "\n")

                    count += 1

                f.close()

            for final_line in candidate_lines:
                final_lines[final_line] = candidate_lines[final_line]

            # This is here for basic validation reasons. If it is triggered, then the mapping has an error
            if max_coverage_count == 0:
                print ("ZERO COVERAGE FOUND: Final lines at this point:", final_lines)
                print ("Cur line:", cur_line)
                exit()
            else:
                coverage_total = len(covered_picked_csns)

            if coverage_total == lines_from_picked:
                break

        # Get the next line
        print (coverage_total, 'vs', lines_from_picked)    
        cur_line = zero_functions.next_combination(cur_line, max_number)

        # if (len(final_lines) >= 10):
           
        #     # print ('record list:')
        #     # for x in temp_records:
        #     #     print (x + ': ' + str(temp_records[x]))
        #     exit()

    print ('final lines:', final_lines)
    end_time = time.time() - start_time
    print ('--- ' + str(convert(end_time)) + ' ---')

    if testmode == False:
        f = open(path + '.progress', "a")
        f.write("*****\nTotal number of lines: " + str(len(final_lines)))
        f.write("\nTime taken: " + str(convert(end_time)) + '\n')
        f.close()

        os.rename(path + '.progress', path + '.txt')


    return final_lines