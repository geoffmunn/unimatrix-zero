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
    #max_coverage_count	= 0
    #max_candidate_line	= []
    #max_current_csns	= set()

    candidate_results = {}

    # Step 2: Go through each subset of $cur_line. These are of size $covered from $picked
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

        # Step 3: Now combine them to lines of length $line_length - these are potential nominated lines
        #quick_exit = False
        for missing_length_subset in missing_length_template:

            # This full line is a candidate for what can cover the current line
            candidate_line = templated_subset[:]
            for j in missing_length_subset:
                candidate_line.append(missing_subset_numbers[j])
            candidate_line.sort()

            #print ("candidate line:",candidate_line)
            # Reset the coverage statistics:
            #coverage_count	= 0
            current_csns 	= set()
            #below_count		= set()

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

                    # If the CSN is below the bottom-most index, then we can assume it's covered
                    # This should be a bit quicker for very large wheels
                    #print (csn,'vs',bottom_index)
                    if csn > bottom_index:
                        if csn not in covered_picked_csns:
                            #print ("adding to covered csns")
                            current_csns.add(csn)
                    

            # The coverage is the total number of CSNs that aren't in the $covered_picked_csns list
            differences 	= current_csns.difference(covered_picked_csns)
            #coverage_count 	= len(differences)

            # if max_possible_coverage == -1:
            #     max_coverage = coverage_count

            candidate_results[' '.join([str(item) for item in candidate_line])] = differences
            # If this is the current best result, then keep a copy of it:
            # if coverage_count > max_coverage_count:
            #     max_coverage_count	= coverage_count
            #     max_candidate_line 	= candidate_line
            #     max_current_csns 	= current_csns

            #     # To save time, we can exit this entire loop if we've found the best possible line
            #     # if coverage_count == max_possible_coverage:
            #     #     quick_exit = True
            #     #     break

        #if quick_exit == True:
        #    break
    
    return candidate_results

def scan(covered_subsets_template: list, covered_subsets_length_template: list, missing_picked_cover_template: list, missing_length_template: list, covered_picked_csns: list, cur_line: list, max_number: int, bottom_index: int):

    # Reset the maximum statistics because we're starting a new line search
    max_coverage_count	= 0
    max_candidate_line	= []
    max_current_csns	= set()

    # Step 2: Go through each subset of $cur_line. These are of size $covered from $picked
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

                    # If the CSN is below the bottom-most index, then we can assume it's covered
                    # This should be a bit quicker for very large wheels
                    #print (csn,'vs',bottom_index)
                    if csn > bottom_index:
                        if csn not in covered_picked_csns:
                            #print ("adding to covered csns")
                            current_csns.add(csn)
                    
            # The coverage is the total number of CSNs that aren't in the $covered_picked_csns list
            differences 	= current_csns.difference(covered_picked_csns)
            coverage_count 	= len(differences)

            # If this is the current best result, then keep a copy of it:
            if coverage_count >= max_coverage_count:
                max_coverage_count	= coverage_count
                max_candidate_line 	= candidate_line
                max_current_csns 	= current_csns

        if quick_exit == True:
            break
    
    return max_coverage_count, max_candidate_line, max_current_csns
        

def create(max_number, line_length, picked, cover, testmode, path):

    version			= '1.3.2'
    start_time		= time.time()
    #max_possible_coverage	= -1
    bottom_index	= 1

    # Dirty workaround alert! I'm not sure how to properly fix this.
    # In the cases of 8 2 2 2, bottom_index needs to be zero
    if picked >= line_length:
       bottom_index = 0

    covered_subsets_template		= zero_functions.covered_subsets_template(picked, cover)
    covered_subsets_length_template	= zero_functions.covered_subsets_length_template(line_length, cover)
    missing_length_template			= zero_functions.missing_length_template(max_number, line_length, picked, cover)
    missing_picked_cover_template	= zero_functions.missing_picked_cover_template(max_number, line_length, picked, cover)

    #print (covered_subsets_template)
    #print (covered_subsets_length_template)
    #print (missing_length_template)
    #print (missing_picked_cover_template)

    #current_csns		= set()
    covered_picked_csns	= set()		# This is the canonical list of picked lines we have covered
    final_lines			= {}		# This is the list of lines we will return with
    lines_from_picked	= comb(max_number, picked)

    temp_records = {}

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
        temp_records = {}
        print ('*********')
        print ('NEW LOOP')
        print ('*********')
        print (i, cur_line)

        # Do not process this line if it's already covered
        if i >= bottom_index and i not in covered_picked_csns:

            # get the best pair.
            # To do this, we need every uncovered candidate, and their coverage:
            first_line = next_line(covered_subsets_template, covered_subsets_length_template, missing_picked_cover_template, missing_length_template, covered_picked_csns, cur_line, max_number, bottom_index)
            
            # A running total of the coverage of the combination so far
            combined_coverage_count = -1
            
            # The lines we've currently picked as being our candidates
            candidate_lines = {}

            # the CSNs that the candidate lines cover
            combined_csns = []

            for line in first_line:

                #print ('**************************')
                #print ('we want to simulate', line, ' which covers ',len(first_line[line]),' CSNs:', first_line[line])

                # Now we need to find the next line available
                cur_line2 = copy.copy(cur_line)

                # This is a combination of all the CSNs from the current line in $first_line, and anything we've definitely covered so far
                temp_covered_picked_csns1 = first_line[line].union(covered_picked_csns)

                # Quit here if this one line covers everything
                if len(temp_covered_picked_csns1) == lines_from_picked:
                    print ('TOTAL COVERAGE FOUND!')
                    candidate_lines = {}
                    #combined_csns = []
                    #combined_csns = first_line[line]
                    combined_csns = temp_covered_picked_csns1
                    candidate_lines[line] = str('{:.2f}'.format(((coverage_total + len(first_line[line]))/lines_from_picked) * 100)) + '%'
                    combined_coverage_count = len(first_line[line])

                    print ('new candidate:')
                    print ('line 1:', line, '(',len(first_line[line]),')')
                    print ('covered CSNs:', combined_csns)
                    print ('combined coverage:', combined_coverage_count)
        
                    for final_line in candidate_lines:
                        final_lines[final_line] = candidate_lines[final_line]

                    print ('FINAL LINES:', final_lines)
                    print (len(final_lines))
                    exit()
    
                else :
                    
                    # Otherwise, go through every line from here and find the first one that's not covered
                    for j in range(i + 1, lines_from_picked + 1):

                        # Get the next line for this combination
                        cur_line2 = zero_functions.next_combination(cur_line2, max_number)    
                
                        # If this is not covered in the CSNs from the first line...
                        if j >= bottom_index and j not in temp_covered_picked_csns1:
                            
                            # This line is not covered, so lets get all its possibilities
                            second_line = next_line(covered_subsets_template, covered_subsets_length_template, missing_picked_cover_template, missing_length_template, temp_covered_picked_csns1, cur_line2, max_number, bottom_index)

                            for line2 in second_line:
                                #print ('line1:', line, '(', len(first_line[line]), ')')
                                #print ('line2:', line2, '(', len(second_line[line2]), ')')
                                # print ('----')

                                # Now we need to find the next line available
                                cur_line3 = copy.copy(cur_line2)

                                # This is a combination of all the CSNs from the current line in $first_line, and anything we've definitely covered so far
                                temp_covered_picked_csns2 = second_line[line2].union(temp_covered_picked_csns1)

                                #combined_csns = []
                                #combined_csns = second_line[line2].union(first_line[line])
                                #combined_coverage_count = len(combined_csns)

                                # Quit here if these two lines cover everything
                                if len(temp_covered_picked_csns2) == lines_from_picked:
                                    print ('TOTAL COVERAGE FOUND!')
                                    candidate_lines = {}
                                    # combined_csns = []
                                    # combined_csns = second_line[line2].union(first_line[line])
                                    combined_csns = temp_covered_picked_csns2
                                    candidate_lines[line] = str('{:.2f}'.format(((coverage_total + len(combined_csns))/lines_from_picked) * 100)) + '%'
                                    combined_coverage_count = len(temp_covered_picked_csns2)

                                    print ('new candidate:')
                                    print ('line 1:', line, '(',len(first_line[line]),')')
                                    print ('line 2:', line2, '(',len(second_line[line2]),')')
                                    print ('covered CSNs:', temp_covered_picked_csns2)
                                    print ('combined coverage:', combined_coverage_count)
                        
                                    for final_line in candidate_lines:
                                        final_lines[final_line] = candidate_lines[final_line]

                                    print ('FINAL LINES:', final_lines)
                                    print (len(final_lines))
                                    exit()

                                else :
                                    

                                    # Ok, so now we have 2 lines and the combined covered CSNs

                                    max_coverage_count, max_candidate_line, max_current_csns = scan(covered_subsets_template, covered_subsets_length_template, missing_picked_cover_template, missing_length_template, temp_covered_picked_csns2, cur_line3, max_number, bottom_index)

                                    temp_covered_picked_csns3 = max_current_csns.union(temp_covered_picked_csns2)
                                    if (len(temp_covered_picked_csns3)) >= combined_coverage_count:
                                        print ('new candidate:')
                                        print ('line 1:', line, '(',len(first_line[line]),')')
                                        print ('line 2:', line2, '(',len(second_line[line2]),')')
                                        print ('line 3:', max_candidate_line, '(',max_coverage_count,')')
                                        #print ('combined coverage:', combined_coverage_count)

                                        combined_coverage_count = len(temp_covered_picked_csns3)
                                        print ('new combined coverage count:', combined_coverage_count)

                                        print ('csns:', len(temp_covered_picked_csns3), temp_covered_picked_csns3)

                                        candidate_lines = {}
                                        candidate_lines[line] = str('{:.2f}'.format((len(temp_covered_picked_csns1)/lines_from_picked) * 100)) + '%'
                                        candidate_lines[line2] = str('{:.2f}'.format((len(temp_covered_picked_csns2)/lines_from_picked) * 100)) + '%'
                                        candidate_lines[' '.join([str(item) for item in max_candidate_line])] = str('{:.2f}'.format((len(temp_covered_picked_csns3)/lines_from_picked) * 100)) + '%'
                                                                                  
                                        combined_csns = temp_covered_picked_csns3
            
            # Update the list of covered CSNs
            for csn in combined_csns:
                if csn >= bottom_index:
                    #if csn not in covered_picked_csns:
                    covered_picked_csns.add(csn)
                    #else:
                    #    print ('CSN alread exists!')
            
            print ('the best combo is:', candidate_lines)
            print ('this combo covers:', combined_csns, '(', len(combined_csns), ')')
            print ('total covered csns:', covered_picked_csns, len(covered_picked_csns))
            
            if testmode == False:
                f = open(path + '.progress', "a")
                count = 1
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
                # Add the max candidate line to the list of final lines
                # final_lines.append(max_candidate_line)

                # # Update the list of covered CSNs
                # for csn in max_current_csns:
                #     if csn >= bottom_index:
                #         covered_picked_csns.add(csn)

                # This is the total number of covered CSNs so far.
                #print ('adding these csns:', covered_picked_csns)
                coverage_total = len(covered_picked_csns)

                
                # Find the new bottom index and remove anything beneath that
                # for j in range(bottom_index + 1, lines_from_picked + 1):
                    
                #     if j in covered_picked_csns:
                #         covered_picked_csns.remove(j)
                #     else:
                #         bottom_index = j
                #         break

                # Write this line to the output file
                # if testmode == False:
                #     f = open(path + '.progress', "a")
                #     #f.write(str(len(final_lines)) + ' (' + str('{:.2f}'.format((coverage_total/lines_from_picked) * 100)) + '%): '  + ' '.join([str(item) for item in pair_candidate_lines]) + "\n")
                #     for final_line in pair_candidate_lines: 
                #         f.write()
                #     f.close()

            # If we have covered all the $picked CSNs, then we can finish!
            # print ('new bottom index:', bottom_index)
            # print (coverage_total, 'vs', lines_from_picked)    
            # print (covered_picked_csns)
            # print ('final lines:', final_lines)

            if coverage_total == lines_from_picked:
                break

        # Get the next line
        print (coverage_total, 'vs', lines_from_picked)    
        cur_line = zero_functions.next_combination(cur_line, max_number)

        # if (len(final_lines) >= 9):
           
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