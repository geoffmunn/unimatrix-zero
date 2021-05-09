#!/usr/bin/env python

import time
from math import comb
from unimatrix_zero import zero_functions

def create(max_number, line_length, picked, cover, testmode, path):

    version 		= '1.3.1'
    start_time 		= time.time()
    bottom_index 	= 1
    max_coverage 	= -1

    covered_subsets_template		= zero_functions.covered_subsets_template(picked, cover)
    covered_subsets_length_template = zero_functions.covered_subsets_length_template(line_length, cover)
    missing_length_template 		= zero_functions.missing_length_template(max_number, line_length, picked, cover)
    missing_picked_cover_template 	= zero_functions.missing_picked_cover_template(max_number, line_length, picked, cover)

    current_csns		= set()
    covered_picked_csns	= set()		# This is the canonical list of picked lines we have covered
    final_lines			= []		# This is the list of lines we will return with
    lines_from_picked 	= comb(max_number, picked)

    # Now start generating some lines!
    if testmode == False:
        f = open(path, "w")
        f.write("Unimatrix Zero\nVersion: " + version + "\n\nRange: " + str(max_number) + "\nLine length: " + str(line_length) + "\nPicked: " + str(picked) + "\nCover: " + str(cover) + "\n\n*****\n")
        f.close()

    # Create the first line:
    cur_line = []
    for j in range(picked, 0, -1):
        cur_line.append(j)

    coverage_total = 0
    # Step 1: Take the next line of $picked length
    for i in range(1, lines_from_picked + 1):

        print ('*********')
        print (i, cur_line)

        # Do not process this line if it's already covered
        if i >= bottom_index and i not in covered_picked_csns:

            # Reset the maximum statistics because we're starting a new line search
            max_coverage_count	= 0
            max_candidate_line 	= []
            max_current_csns 	= set()

            # Step 2: Go through each subset of $cur_line. These are of size $covered from $picked
            # $covered cannot be larger than $line_length (or $picked)
            loop_count 	= 0
            loop_max 	= len(covered_subsets_template)
            for subset in covered_subsets_template:
                loop_count += 1
                print (loop_count,'of',loop_max,'covered subsets')

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

                # Step 3: Now combine them to lines of length $line_length - these are potential nominated lines
                quick_exit = False
                for missing_length_subset in missing_length_template:

                    # This full line is a candidate for what can cover the current line
                    candidate_line = templated_subset[:]
                    for j in missing_length_subset:
                        candidate_line.append(missing_subset_numbers[j])
                    candidate_line.sort()

                    # Reset the coverage statistics:
                    coverage_count	= 0
                    current_csns 	= set()
                    below_count		= set()

                    # Step 4: Go through each covered subset (length = line_length) in the candidate line
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

                            # If the CSN is below the bottom-most index, then we can assume it's covered
                            # This should be a bit quicker for very large wheels
                            if csn >= bottom_index:
                                if csn not in covered_picked_csns:
                                    current_csns.add(csn)
                            else:
                                below_count.add(csn)

                    # The coverage is the total number of CSNs that aren't in the $covered_picked_csns list
                    differences 	= current_csns.difference(covered_picked_csns)
                    coverage_count 	= len(differences)

                    if max_coverage == -1:
                        max_coverage = coverage_count

                    # If this is the current best result, then keep a copy of it:
                    if coverage_count > max_coverage_count:
                        max_coverage_count	= coverage_count
                        max_candidate_line 	= candidate_line
                        max_current_csns 	= current_csns

                        # To save time, we can exit this entire loop if we've found the best possible line
                        if coverage_count == max_coverage:
                            quick_exit = True
                            break

                if quick_exit == True:
                    break

            # This is here for basic validation reasons. If it is triggered, then the mapping has an error
            if max_coverage_count == 0:
                print ("ZERO COVERAGE FOUND: Final lines at this point:", final_lines)
                print ("Cur line:", cur_line)
                exit()
            else:
                # Add the max candidate line to the list of final lines
                final_lines.append(max_candidate_line)

                # Update the list of covered CSNs
                for csn in max_current_csns:
                    if csn >= bottom_index:
                        covered_picked_csns.add(csn)

                # This is the total number of covered CSNs so far.
                coverage_total += len(max_current_csns)

                # Find the new bottom index and remove anything beneath that
                for j in range(bottom_index, lines_from_picked + 1):
                    if j in covered_picked_csns:
                        covered_picked_csns.remove(j)
                    else:
                        bottom_index = j
                        break

                # Write this line to the output file
                if testmode == False:
                    f = open(path, "a")
                    f.write(str(len(final_lines)) + ' (' + str(round((coverage_total/lines_from_picked) * 100, 2)) + '%): '  + ' '.join([str(item) for item in max_candidate_line]) + "\n")
                    f.close()

            # If we have covered all the $picked CSNs, then we can finish!
            if coverage_total == lines_from_picked:
                break;

        # Get the next line
        cur_line = zero_functions.next_combination(cur_line, max_number)

    end_time = time.time() - start_time
    print("--- %s seconds ---" %end_time )

    if testmode == False:
        f = open(path, "a")
        f.write("*****\nTotal number of lines: " + str(len(final_lines)))
        f.write("\nTime taken: " + str(end_time))
        f.close()

    return final_lines