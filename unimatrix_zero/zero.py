#!/usr/bin/env python

import time
import os
import copy
from math import comb
from unimatrix_zero import zero_functions

def convert(seconds:int):
    '''
    This returns the provided seconds in a human readable form.
    '''

    status 			 = ''
    seconds 		 = round(seconds, 2)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes   = divmod(minutes, 60)

    periods 	= [('hours', hours), ('minutes', minutes), ('seconds', seconds)]
    time_string = ', '.join('{} {}'.format(value, name) for name, value in periods if value)

    result = '{} {}'.format(status, time_string).strip()

    if result == '':
        result = '0.01 seconds'

    return result

def potential_lines(covered_subsets_template: list, covered_subsets_length_template: list, missing_picked_cover_template: list, missing_length_template: list, covered_picked_csns: list, cur_line: list, max_number: int):
    '''
    This function returns all the uncovered lines that cover the provided $cur_line, and the CSNs that are covered by each one.
    '''

    # This will hold the result we like the most.
    candidate_results = {}

    # Step 1: Go through each subset of $cur_line. These are of size $covered from $picked.
    # $covered cannot be larger than $line_length (or $picked).
    for subset in covered_subsets_template:
        
        # Map each number in $cur_line to a spot in the subset template.
        templated_subset = []
        for j in subset:
            templated_subset.append(cur_line[j])

        # Find the missing numbers from this subset.
        missing_subset_numbers = []
        for j in range(1, max_number + 1):
            if j not in templated_subset:
                missing_subset_numbers.append(j)

        # So now we have the missing numbers for the actual subset of the current line.
        # Together the length of this missing numeber set + the templated subset should add up to $line_length.

        # Step 2: Now combine them to lines of length $line_length - these are potential nominated lines
        for missing_length_subset in missing_length_template:

            # This full line is a candidate for what can cover the current line
            candidate_line = templated_subset[:]
            for j in missing_length_subset:
                candidate_line.append(missing_subset_numbers[j])
            candidate_line.sort()

            # Reset the coverage statistics:
            current_csns = set()
            
            # Step 3: Go through each covered subset (length = line_length) in the candidate line
            for covered_subset in covered_subsets_length_template:

                # Map each spot in the subset to a $candidate_line number
                templated_covered_subset = []
                for j in covered_subset:
                    templated_covered_subset.append(candidate_line[j])
                templated_covered_subset.sort()

                # Find the missing numbers from this subset
                missing_candidate_subset_numbers = []
                for j in range(1, max_number + 1):
                    if j not in templated_covered_subset:
                        missing_candidate_subset_numbers.append(j)

                # Step 4: Now build this up to $picked
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
                    if csn not in covered_picked_csns:
                        current_csns.add(csn)
                    
            # The coverage is the total number of CSNs that aren't in the $covered_picked_csns list
            differences = current_csns.difference(covered_picked_csns)
            
            candidate_results[' '.join([str(item) for item in candidate_line])] = differences
            
    return candidate_results

def get_best_line(covered_subsets_template: list, covered_subsets_length_template: list, missing_picked_cover_template: list, missing_length_template: list, covered_picked_csns: list, cur_line: list, max_number: int):
    '''
    This returns the best possible line for the provided $cur_line value.
    It also returns the covered CSNs and the coverage of this suggested line
    '''
    
    max_coverage_count	= 0
    max_candidate_line	= []
    max_current_csns	= set()

    # Step 1: Go through each subset of $cur_line. These are of size $covered from $picked
    # $covered cannot be larger than $line_length (or $picked)
    for subset in covered_subsets_template:
        # Map each number in $cur_line to a spot in the subset template
        templated_subset = []
        for j in subset:
            templated_subset.append(cur_line[j])

        # Find the missing numbers from this subset
        missing_subset_numbers = []
        for j in range(1, max_number + 1):
            if j not in templated_subset:
                missing_subset_numbers.append(j)

        # So now we have the missing numbers for the actual subset of the current line
        # Together they should add up to $line_length

        # Step 2: Now combine them to lines of length $line_length - these are potential nominated lines
        for missing_length_subset in missing_length_template:

            # This full line is a candidate for what can cover the current line
            candidate_line = templated_subset[:]
            for j in missing_length_subset:
                candidate_line.append(missing_subset_numbers[j])
            candidate_line.sort()

            # Reset the coverage statistics:
            coverage_count = 0
            current_csns   = set()

            # Step 3: Go through each covered subset (length = line_length) in the candidate line
            for covered_subset in covered_subsets_length_template:

                # Map each spot in the subset to a $candidate_line number
                templated_covered_subset = []
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

                    # If this CSN is not in the currently covered list, then add it to the total for this suggested line
                    if csn not in covered_picked_csns:
                        current_csns.add(csn)
                    
            # The coverage is the total number of CSNs that aren't in the $covered_picked_csns list
            differences    = current_csns.difference(covered_picked_csns)
            coverage_count = len(differences)

            # If this is the current best result, then keep a copy of it
            # NOTE: this can be either >= or >
            if coverage_count >= max_coverage_count:
                max_coverage_count = coverage_count
                max_candidate_line = candidate_line
                max_current_csns   = current_csns

    return max_coverage_count, max_candidate_line, max_current_csns
        
def create(max_number, line_length, picked, cover, testmode, path):

    # Basic meta information
    version	   = '1.4.0'
    start_time = time.time()

    # Create the basic templates
    covered_subsets_template		= zero_functions.covered_subsets_template(picked, cover)
    covered_subsets_length_template	= zero_functions.covered_subsets_length_template(line_length, cover)
    missing_length_template			= zero_functions.missing_length_template(max_number, line_length, picked, cover)
    missing_picked_cover_template	= zero_functions.missing_picked_cover_template(max_number, line_length, picked, cover)

    covered_picked_csns	= set() # This is the canonical list of picked lines we have covered
    final_lines			= {}	# This is the list of lines we will return with

    total_lines_from_picked	= comb(max_number, picked) # This is the total number of lines we need to cover (not the actual lines)
    coverage_total          = 0  # The total number of lines we've covered so far

    # Create the progress file
    if testmode == False:
        f = open(path + '.progress', "w")
        f.write("Unimatrix Zero\nVersion: " + version + "\n\nRange:       " + str(max_number) + "\nLine length: " + str(line_length) + "\nPicked:      " + str(picked) + "\nCover:       " + str(cover) + "\n\n*****\n")
        f.close()

    # Now start generating some lines!

    # Create the first line. This assumes we start with CSN 1 -  1 2 3 4 5 6 (for example)
    cur_line = []
    for j in range(picked, 0, -1):
        cur_line.append(j)

    # Step 1: Take the next line of $picked length
    for i in range(1, total_lines_from_picked + 1):
        
        # Do not process this line if it's already covered
        if i not in covered_picked_csns:

            # Get the best pair of lines.
            # To do this, we need every uncovered candidate, and their coverage.

            # This are all the potential lines and their covered CSNs:
            best_lines = potential_lines(covered_subsets_template, covered_subsets_length_template, missing_picked_cover_template, missing_length_template, covered_picked_csns, cur_line, max_number)

            combined_coverage_count = -1
            pair_candidate_lines    = {}
            combined_csns           = []

            for line in best_lines:

                # Now we need to find the next potential line.
                
                # Take a copy of the current line so we can work off that.
                cur_line2 = copy.copy(cur_line)

                # This is the combination of the existing (covered) CSNs and whatever the current best line ($line) covers
                temp_covered_picked_csns = best_lines[line].union(covered_picked_csns)

                if len(temp_covered_picked_csns) == total_lines_from_picked:
                    pair_candidate_lines       = {}
                    combined_csns              = []
                    combined_csns              = best_lines[line]
                    pair_candidate_lines[line] = str('{:.2f}'.format(((coverage_total + len(best_lines[line]))/total_lines_from_picked) * 100)) + '%'
                    combined_coverage_count    = len(best_lines[line])

                    break
        
                else :
                    for j in range(i + 1, total_lines_from_picked + 1):

                        # Output some details so we can see some progress
                        print (f'{coverage_total}/{total_lines_from_picked} ({i}:{j})', end='\r')

                        # Get the next line based on the current line (by CSN order):
                        cur_line2 = zero_functions.next_combination(cur_line2, max_number)    

                        if j not in temp_covered_picked_csns:
                            max_coverage_count, max_candidate_line, max_current_csns = get_best_line(covered_subsets_template, covered_subsets_length_template, missing_picked_cover_template, missing_length_template, temp_covered_picked_csns, cur_line2, max_number)

                            # NOTE: this can be either >= or >
                            if max_coverage_count + len(best_lines[line]) > combined_coverage_count:

                                # This are all the CSNs that are covered with this current best line + the scan results
                                combined_csns = max_current_csns.union(best_lines[line])

                                pair_candidate_lines = {}

                                # This is the current potential line
                                pair_candidate_lines[line] = str('{:.2f}'.format(((coverage_total + len(best_lines[line]))/total_lines_from_picked) * 100)) + '%'
                                
                                # And this is the best line that matches the potential line
                                pair_candidate_lines[' '.join([str(item) for item in max_candidate_line])] = str('{:.2f}'.format(((coverage_total + len(combined_csns)) / total_lines_from_picked) * 100)) + '%'

                                # Update the combined count with the total of this pair - it is the new best combination of lines
                                combined_coverage_count = max_coverage_count + len(best_lines[line])

            # Update the list of covered CSNs
            for csn in combined_csns:
                covered_picked_csns.add(csn)
            
            if testmode == False:
                f = open(path + '.progress', "a")
                count = 1
                for final_line in pair_candidate_lines: 
                    f.write(str(len(final_lines) + count) + ' (' + pair_candidate_lines[final_line] + '): ' + final_line + "\n")

                    count += 1

                f.close()

            for final_line in pair_candidate_lines:
                final_lines[final_line] = pair_candidate_lines[final_line]

            # This is here for basic validation reasons. If it is triggered, then the mapping has an error
            if max_coverage_count == 0:
                print ("ZERO COVERAGE FOUND: Final lines at this point:", final_lines)
                print ("Cur line:", cur_line)
                exit()
            else:
                # This is the total number of covered CSNs so far.
                coverage_total = len(covered_picked_csns)

            # If we have covered all the $picked CSNs, then we can finish!
            if coverage_total == total_lines_from_picked:
                break

        # Get the next line
        cur_line = zero_functions.next_combination(cur_line, max_number)

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