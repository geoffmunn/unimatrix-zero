#!/usr/bin/env python

import time
import os
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

def prepare_line(subset, cur_line, max_number):
    # Map each number in $cur_line to a spot in the subset template
    templated_subset = []
    for j in subset:
        templated_subset.append(cur_line[j])

    # Find the missing numbers from this subset
    missing_subset_numbers = []
    for j in range(1, max_number + 1):
        if j not in templated_subset:
            missing_subset_numbers.append(j)

    return templated_subset, missing_subset_numbers

def get_candidate_line(templated_subset, missing_length_subset, missing_subset_numbers, covered_subsets_length_template, missing_picked_cover_template, max_number, covered_picked_csns):
    # This full line is a candidate for what can cover the current line
    candidate_line = templated_subset[:]
    for j in missing_length_subset:
        candidate_line.append(missing_subset_numbers[j])
    candidate_line.sort()

    #print ("candidate line:",candidate_line)
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

        #print ("Templated covered subset:",templated_covered_subset)
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

            #print ("Covered picked line:",covered_picked_line)
            # This full line is a candidate for what can cover $cur_line
            # Get the CSN so we can check if we've already got it:
            csn = zero_functions.sequence_number(covered_picked_line, max_number)

            #print ("csn of picked line", csn)
            # If the CSN is below the bottom-most index, then we can assume it's covered
            # This should be a bit quicker for very large wheels
            #if csn > bottom_index:
            if csn not in covered_picked_csns:
                current_csns.add(csn)
            #else:
            #    below_count.add(csn)

    # The coverage is the total number of CSNs that aren't in the $covered_picked_csns list
    differences 	= current_csns.difference(covered_picked_csns)
    coverage_count 	= len(differences)

    return coverage_count, candidate_line, current_csns

def update_record(max_candidate_line, max_current_csns, covered_picked_csns, lines_from_picked, coverage_total):

    # Update the list of covered CSNs
    for csn in max_current_csns:
        #if csn >= bottom_index:
        covered_picked_csns.add(csn)

    # This is the total number of covered CSNs so far.
    coverage_total += len(max_current_csns)

    #print ("update record covered_picked_csns", covered_picked_csns)
    # Find the new bottom index and remove anything beneath that
    #for j in range(bottom_index+1, lines_from_picked + 1):
    #for j in range(0, lines_from_picked + 1):
        #print ("bottom index checking", j)
    #    if j in covered_picked_csns:
    #        covered_picked_csns.remove(j)
        #else:
        #    #print (j, 'not in list, exiting')
        ##    bottom_index = j
    #        break

    #print ("updated record bottom index:", bottom_index)
    #return covered_picked_csns, coverage_total, bottom_index
    return covered_picked_csns, coverage_total

def create(max_number, line_length, picked, cover, testmode, path):

    version			= '1.3.2'
    start_time		= time.time()
    max_coverage	= -1
    #bottom_index	= 1
    depth			= 2

    # Dirty workaround alert! I'm not sure how to properly fix this.
    # In the cases of 8 2 2 2, bottom_index needs to be zero
    #if picked >= line_length:
    #    bottom_index = 0

    covered_subsets_template		= zero_functions.covered_subsets_template(picked, cover)
    covered_subsets_length_template	= zero_functions.covered_subsets_length_template(line_length, cover)
    missing_length_template			= zero_functions.missing_length_template(max_number, line_length, picked, cover)
    missing_picked_cover_template	= zero_functions.missing_picked_cover_template(max_number, line_length, picked, cover)
    matrix 			 				= zero_functions.matrix_template(len(covered_subsets_template), depth)

    current_csns		= set()
    covered_picked_csns	= set()		# This is the canonical list of picked lines we have covered
    final_lines			= []		# This is the list of lines we will return with
    lines_from_picked	= comb(max_number, picked)





    # Now start generating some lines!
    if testmode == False:
        f = open(path + '.progress', "w")
        f.write("Unimatrix Zero\nVersion: " + version + "\n\nRange:       " + str(max_number) + "\nLine length: " + str(line_length) + "\nPicked:      " + str(picked) + "\nCover:       " + str(cover) + "\n\n*****\n")
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
        #if i >= bottom_index and i not in covered_picked_csns:
        if i not in covered_picked_csns:

            # Reset the maximum statistics because we're starting a new line search
            max_coverage_count	= 0
            max_candidate_line	= []
            max_current_csns	= set()

            # Step 2: Go through each subset of $cur_line. These are of size $covered from $picked
            # $covered cannot be larger than $line_length (or $picked)
            loop_count1	= 0
            loop_count2	= 0
            loop_max	= len(covered_subsets_template)

            for subset in covered_subsets_template:

                loop_count1 += 1
                print (loop_count1,'of',loop_max,'covered subsets')

                # Map each number in $cur_line to a spot in the subset template
                templated_subset, missing_subset_numbers = prepare_line(subset, cur_line, max_number)

                # So now we have the missing numbers for the actual subset of the current line
                # Together they should add up to $line_length

                # Step 3: Now combine them to lines of length $line_length - these are potential nominated lines
                loop_index_x = 0
                for missing_length_subset in missing_length_template:
                    loop_index_x += 1

                    covered_picked_csns_x = covered_picked_csns.copy()

                    #print ("ORIGINAL BOTTOM INDEX:", bottom_index)

                    #bottom_index_x = bottom_index

                    coverage_count_x, candidate_line_x, current_csns_x = get_candidate_line(templated_subset, missing_length_subset, missing_subset_numbers, covered_subsets_length_template, missing_picked_cover_template, max_number, covered_picked_csns_x)

                    #print ('coverage count x', coverage_count_x)
                    #print ('candidate_line x', candidate_line_x)
                    #print ('current csns_x', current_csns_x)

                    covered_picked_csns_x, coverage_total_x = update_record(candidate_line_x, current_csns_x, covered_picked_csns_x, lines_from_picked, coverage_total)

                    # Now loop again for a double line combo
                    cur_line_y = cur_line[:]
                    cur_line_y = zero_functions.next_combination(cur_line_y, max_number)

                    for j in range(i + 1, lines_from_picked + 1):

                        # Do not process this line if it's already covered
                        #if j not in covered_picked_csns_x:
                        if True:
                            print ('inner loop *********')
                            print (j, cur_line_y)
                            print ('x coverage:', coverage_total_x)
                            loop_count_y = 0
                            for subset_y in covered_subsets_template:

                                loop_count_y += 1
                                print (loop_count_y,'of',loop_max,'covered subsets')

                                # Map each number in $cur_line to a spot in the subset template
                                templated_subset_y, missing_subset_numbers_y = prepare_line(subset_y, cur_line_y, max_number)

                                #print ("templated subset:",templated_subset_y)
                                loop_index_y = 0
                                for missing_length_subset_y in missing_length_template:
                                    loop_index_y += 1
                                    #print ('x coverage:', coverage_total_x)

                                    #print ('templated_subset_y',templated_subset_y)
                                    #print ('missing length subset y', missing_length_subset_y)
                                    #print ('missing subset numbers y', missing_subset_numbers_y)
                                    print ('covered picked csns x', covered_picked_csns_x)

                                    coverage_count_y, candidate_line_y, current_csns_y = get_candidate_line(templated_subset_y, missing_length_subset_y, missing_subset_numbers_y, covered_subsets_length_template, missing_picked_cover_template, max_number, covered_picked_csns_x)

                                    covered_picked_csns_y, coverage_total_y = update_record(candidate_line_y, current_csns_y, covered_picked_csns_x, lines_from_picked, coverage_total_x)

                                    print ('covered picked csns y', covered_picked_csns_y)
                                    print (candidate_line_y)
                                    print (coverage_count_y)
                                    print (coverage_total_y)

                            exit()
                            # Reset the maximum statistics because we're starting a new line search
                        #    max_coverage_count	= 0
                        #    max_candidate_line	= []
                        #    max_current_csns	= set()

                            # Step 2: Go through each subset of $cur_line. These are of size $covered from $picked
                            # $covered cannot be larger than $line_length (or $picked)
                        #    loop_count1	= 0
                        #    loop_count2	= 0
                        #    loop_max	= len(covered_subsets_template)

                            #covered_picked_csns_x = covered_picked_csns.copy()

                        #    for subset in covered_subsets_template:
                            #for x in matrix:
                                #subset = covered_subsets_template[x[0]]

                        #        loop_count1 += 1
                        #        print (loop_count1,'of',loop_max,'covered subsets')

                                # Map each number in $cur_line to a spot in the subset template
                        #        templated_subset, missing_subset_numbers = prepare_line(subset, cur_line, max_number)

                                # So now we have the missing numbers for the actual subset of the current line
                                # Together they should add up to $line_length

                                # Step 3: Now combine them to lines of length $line_length - these are potential nominated lines
                        #        loop_index_x = 0
                        #        for missing_length_subset in missing_length_template:
                        #            loop_index_x += 1

                        #            covered_picked_csns_x = covered_picked_csns.copy()

                        #            coverage_count_x, candidate_line_x, current_csns_x = get_candidate_line(templated_subset, missing_length_subset, missing_subset_numbers, covered_subsets_length_template, missing_picked_cover_template, max_number, covered_picked_csns_x)

                        #            covered_picked_csns_x, coverage_total_x = update_record(final_lines, candidate_line_x, current_csns_x, covered_picked_csns, lines_from_picked, coverage_total)

                        cur_lineY = zero_functions.next_combination(cur_line_y, max_number)

                    exit()
            covered_picked_csns = covered_picked_csns_x.copy()

            print ("Best line:",max_candidate_line,"(index:",max_candidate_line_index,")")

            covered_picked_csns, coverage_total = update_record(final_lines, max_candidate_line, max_current_csns, covered_picked_csns, lines_from_picked, coverage_total)

            # Add the max candidate line to the list of final lines
            final_lines.append(max_candidate_line)

            # Write this line to the output file
            if testmode == False:
                f = open(path + '.progress', "a")
                f.write(str(len(final_lines)) + ' (' + str('{:.2f}'.format((coverage_total/lines_from_picked) * 100)) + '%): '  + ' '.join([str(item) for item in max_candidate_line]) + "\n")
                f.close()

            # If we have covered all the $picked CSNs, then we can finish!
            if coverage_total == lines_from_picked:
                break;

        # Get the next line
        cur_line = zero_functions.next_combination(cur_line, max_number)

    end_time = time.time() - start_time
    print ('--- ' + str(convert(end_time)) + ' ---')

    if testmode == False:
        f = open(path + '.progress', "a")
        f.write("*****\nTotal number of lines: " + str(len(final_lines)))
        f.write("\nTime taken: " + str(convert(end_time)) + '\n')
        f.close()

        os.rename(path + '.progress', path + '.txt')


    return final_lines