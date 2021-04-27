#!/usr/bin/env python

import sys # Required so we can pass arguments
from math import comb

import time
start_time = time.time()

def sequence_number(cur_line, max_number):

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
            index -= 1

        for i in reversed(range(index)):
            cur_line[i] = cur_line[i + 1] + 1

    return cur_line

def new_template(length):
    cur_subset = []
    for j in range(length, 0, -1):
        cur_subset.append(j - 1)

    return cur_subset

def summary(covered_csns, lines_from_picked, final_lines):

    print (final_lines)
    print ("Count:", len(final_lines))
    print (len(covered_csns),'/',lines_from_picked)

    for i in range(1, lines_from_picked+1):
        if i not in covered_csns:
            print (i, ' is not present!')

    print ("all done!")

###################################

version = "1.2"

test_case = ''
if len(sys.argv) == 2:
    test_case = sys.argv[1]

elif len(sys.argv) == 5:
    max_number 	= int(sys.argv[1])
    line_length	= int(sys.argv[2])
    picked 		= int(sys.argv[3])
    cover 		= int(sys.argv[4])

else:
    # User defined variables
    max_number 	= 10
    line_length	= 6
    picked 		= 6
    cover 		= 5

if test_case == 'test1':
    # Test 1: Basic 1
    max_number 	= 10
    line_length	= 6
    picked 		= 6
    cover 		= 5
elif test_case == 'test2':
    # Test 2:
    max_number 	= 10
    line_length	= 6
    picked 		= 6
    cover 		= 4
elif test_case == 'test3':
    # Test 3:
    max_number 	= 10
    line_length	= 6
    picked 		= 7
    cover 		= 5
elif test_case == 'test4':
    # Test 4:
    max_number 	= 10
    line_length	= 6
    picked 		= 7
    cover 		= 4
elif test_case == 'test5':
    # Test 5:
    max_number 	= 10
    line_length	= 6
    picked 		= 5
    cover 		= 5
elif test_case == 'test6':
    # Test 5:
    max_number 	= 10
    line_length	= 6
    picked 		= 4
    cover 		= 4
elif test_case == 'test7':
    # Test 6:
    max_number 	= 10
    line_length	= 6
    picked 		= 5
    cover 		= 4
elif test_case == 'test8':
    # Test 6:
    max_number 	= 10
    line_length	= 6
    picked 		= 4
    cover 		= 3
elif test_case == 'test9':
    # Test 7:
    max_number 	= 10
    line_length	= 3
    picked 		= 6
    cover 		= 3
elif test_case == 'test10':
    max_number	= 10
    line_length = 3
    picked		= 5
    cover		= 2

###################################

covered_subsets_template		= []
covered_subsets_length_template = []
covered_subsets_picked_template = []
missing_length_template 		= []
missing_picked_template 		= []
missing_picked_cover_template 	= []

current_length_csns		= set()
covered_picked_csns 	= set()		# This is the canonical list of picked lines we have covered
covered_length_csns 	= set()		# This is the canonical list of line lengths we have covered
final_lines				= []		# This is the list of lines we will return with

lines_from_picked 		= comb(max_number, picked)
lines_from_length 		= comb(max_number, line_length)
picked_from_length  	= comb(line_length, picked)
subsets_from_picked 	= comb(picked, cover)
subsets_from_length 	= comb(line_length, cover)
missing_length 			= comb(max_number - cover, line_length - cover)

if picked >= line_length:
    # This works with:
    # 15 3 5 2
    # DOES NOT WORK WITH:
    # 8,3,4,3

    #max_number 	= 10
    #line_length	= 6
    #picked 		= 7
    #cover	 		= 4

    # Good: 10, 3, 5, 2
    # Bad:  10, 6, 7, 4
    #print ("BOO")
    #print ("line length:",line_length)
    #print ("picked:",picked)
    #print ("cover:",cover)

    if picked - line_length == 1:
        #print ("HIHI")
        # Works with: 10, 6, 7, 4
        missing_picked 		= comb(max_number - line_length, picked - line_length)
    else:
        # Works with: 15, 3, 5, 2
        missing_picked 		= comb(max_number - cover - 1, picked - cover - 1)

else:
    missing_picked 		= -1

missing_picked_cover 	= comb(max_number - cover, picked - cover)

#print ("Missing picked:",missing_picked)
###################################
# Build up the template for covered subsets of the picked numbers

cur_subset = new_template(cover)
for i in range(subsets_from_picked):
    covered_subsets_template.append(cur_subset[:])
    cur_subset = next_combination(cur_subset, picked - 1)
###################################

#print ("covered_subsets_template")
#print (covered_subsets_template)

###################################
# Build up the template for covered subsets of the length numbers

cur_subset = new_template(cover)
for i in range(subsets_from_length):
    covered_subsets_length_template.append(cur_subset[:])
    cur_subset = next_combination(cur_subset, line_length - 1)
###################################

#print ("covered_subsets_length_template")
#print (covered_subsets_length_template)

###################################
# Now create the template of the missing combinations for the picked line based on the line length
# We need special accomodations for when picked is less than or equal to the line length or cover

if picked > line_length:
    if picked > cover:
        cur_subset = new_template(picked - line_length)
        for i in range(missing_picked):
            print(i, cur_subset)
            missing_picked_template.append(cur_subset[:])
            #cur_subset = next_combination(cur_subset, max_number - picked)
            cur_subset = next_combination(cur_subset, max_number - line_length - 1)
    else:
        missing_picked_template = [[]]
else:
    if picked < line_length:
        cur_subset = new_template(picked)
        for i in range(picked_from_length):
            covered_subsets_picked_template.append(cur_subset[:])
            cur_subset = next_combination(cur_subset, picked)
    else:
        missing_picked_template = [[]]
###################################

#print ("missing_picked_template")
#print (missing_picked_template)

###################################
# Now create the template of the missing combinations for the line length numbers
# We need special accomodations for when picked is less than or equal to the line length or cover

if line_length > cover:
    cur_subset = new_template(line_length - cover)
    if picked > line_length:
        if picked > cover:
            for i in range(missing_length):
                missing_length_template.append(cur_subset[:])
                cur_subset = next_combination(cur_subset, max_number - cover - 1) 	#-1 is required for 8, 6, 7, 4
        else:
            missing_length_template = [[]]
    else:
        for i in range(missing_length):
            missing_length_template.append(cur_subset[:])
            cur_subset = next_combination(cur_subset, max_number - cover - 1)
else:
    missing_length_template = [[]]
###################################

#print ("missing_length_template")
#print (missing_length_template)

###################################
# Lastly create the template of missing combinations between cover and picked

if picked > line_length:
    cur_subset = new_template(picked - cover)
    for i in range(missing_picked_cover):
        missing_picked_cover_template.append(cur_subset[:])
        cur_subset = next_combination(cur_subset, max_number - cover - 1)
else:
    if picked > cover:
        cur_subset = new_template(picked - cover)
        for i in range(missing_picked_cover):
            missing_picked_cover_template.append(cur_subset[:])
            cur_subset = next_combination(cur_subset, max_number - cover - 1)
    else:
        missing_picked_cover_template = [[]]
###################################

#print ("missing_picked_cover_template")
#print (missing_picked_cover_template)
#exit()

# Now start generating some lines!
file_name = "Combo " + str(max_number) + " " + str(line_length) + " " + str(picked) + " " + str(cover) + ".txt"

f = open(file_name, "w")
f.write("Range: " + str(max_number) + "\nLine length: " + str(line_length) + "\nPicked: " + str(picked) + "\nCover: " + str(cover) + "\nVersion:" + version + "\n\n*****\n")
f.close()

# Create the first line:
cur_line = []
for j in range(picked, 0, -1):
    cur_line.append(j)

# Step 1: Take the next line or $picked length
for i in range(1, lines_from_picked + 1):

    print ('*********')
    print (i, cur_line)

    # Do not process this line if it's already covered
    if i not in covered_picked_csns:

        # Reset the maximum statistics because we're starting a new line search

        max_coverage_count		= 0
        max_candidate_line 		= []
        max_current_length_csns = set()

        # Go through each subset of $cur_line. These are of size $covered from $picked
        # Step 2: Take each subset of size $cover
        x1 = 0
        for subset in covered_subsets_template:
            x1 += 1
            print (x1,'of',len(covered_subsets_template),'covered subsets (outer)')
            # Map each number in $cur_line to a spot in the subset template
            templated_subset = []
            for j in subset:
                templated_subset.append(cur_line[j])

            #print ("templated subset:",templated_subset)

            # Now go through all the subsets of $line_length from $picked
            # Find the missing numbers from this subset
            missing_subset_numbers = []
            for j in range(1, max_number + 1):
                if j not in templated_subset:
                    missing_subset_numbers.append(j)

            # So now we have the missing numbers for the actual subset of the current line
            # Together they should add up to $line_length
            # Now build this up to lines of length $line_length - these are potential nominated lines
            # Step 3: Build this up to each parent set of $line_length
            x2 = 0
            for missing_length_subset in missing_length_template:
                x2 += 1
                print (x2,'of',len(missing_length_template),'missing length template')
                # This full line is a candidate for what can cover the current line
                candidate_line = templated_subset[:]
                for j in missing_length_subset:
                    candidate_line.append(missing_subset_numbers[j])
                candidate_line.sort()

                missing_picked_numbers = []
                for j in range(1, max_number + 1):
                    if j not in candidate_line:
                        missing_picked_numbers.append(j)

                #print ("Candidate line:",candidate_line)

                # Reset the coverage statistics:
                coverage_count 		= 0
                current_length_csns = set()

                x3 = 0
                for covered_subset in covered_subsets_length_template:
                    x3 += 1
                    print(x3,'of',len(covered_subsets_length_template),'covered subsets length template')
                    # Map each number in $cur_line to a spot in the subset template (length = cover)
                    templated_covered_subset = []
                    for j in covered_subset:
                        templated_covered_subset.append(candidate_line[j])
                    templated_covered_subset.sort()

                    #print ("covered subset:",templated_covered_subset)

                    # Now build this up to $picked
                    # Find the missing numbers from this subset
                    missing_candidate_subset_numbers = []
                    for j in range(1, max_number + 1):
                        if j not in templated_covered_subset:
                            missing_candidate_subset_numbers.append(j)

                    x4 = 0
                    for missing_picked_cover_subset in missing_picked_cover_template:
                        x4 +=1
                        print(x4,'of',len(missing_picked_cover_template),'missing picked cover template')
                        # This full line is a candidate for what can cover the current line
                        covered_line = templated_covered_subset[:]
                        for j in missing_picked_cover_subset:
                            covered_line.append(missing_candidate_subset_numbers[j])
                        covered_line.sort()

                        #print ("Full covered line:", covered_line)

                        csn = sequence_number(covered_line, max_number)
                        current_length_csns.add(csn)



                differences = current_length_csns.difference(covered_length_csns)
                coverage_count = len(differences)

                #print (coverage_count)
                #exit()
                if coverage_count >= max_coverage_count:
                    max_coverage_count 		= coverage_count
                    max_candidate_line 		= candidate_line
                    max_current_length_csns = current_length_csns


        #print ("Current picked combo is:", cur_line)
        #print ("The best line is", max_candidate_line, "which covers", max_coverage_count,"lines")
        #print ("This covers the following CSNs:",max_current_length_csns)
        #exit()

        if max_coverage_count == 0:
            print ("ZERO COVERAGE FOUND: Final lines at this point:", final_lines)
            print ("Cur line:", cur_line)
            exit()
        else:
            # Add the max candidate line to the list, and all the coverage statistics
            final_lines.append(max_candidate_line)

            if picked < line_length:
                for csn in max_current_length_csns:
                    covered_picked_csns.add(csn)
            else :
                if line_length == cover:
                    ################### start

                    # in this scenario, we only want to add subsets of the actual current line
                    for subset in covered_subsets_template:
                        # Map each number in $cur_line to a spot in the subset template
                        templated_subset = []
                        for j in subset:
                            templated_subset.append(cur_line[j])

                        # Now go through all the subsets of $line_length from $picked
                        # Find the missing numbers from this subset
                        missing_subset_numbers = []
                        for j in range(1, max_number + 1):
                            if j not in templated_subset:
                                missing_subset_numbers.append(j)

                        # So now we have the missing numbers for the actual subset of the current line
                        # Together they should add up to $line_length
                        # Now build this up to lines of length $line_length - these are potential nominated lines

                        for missing_length_subset in missing_length_template:
                            # This full line is a candidate for what can cover the current line
                            candidate_cover = templated_subset[:]
                            for j in missing_length_subset:
                                candidate_cover.append(missing_subset_numbers[j])
                            candidate_cover.sort()

                            covered_csn = sequence_number(candidate_cover, max_number)
                            covered_length_csns.add(covered_csn)

                    ################### end
                else:
                    for csn in max_current_length_csns:
                        covered_length_csns.add(csn)

            # We need to update the covered csns of picked length so the scan doesn't try covered lines
            # Given the max_candidate_line, we need to get the subsets and then all picked lines that match
            # Build up the candidate line to the various picked length lines

            #print ("Candidate line:", max_candidate_line)
            for subset in covered_subsets_length_template:

                # Map each number in cur_line to a spot in the subset template
                templated_subset = []
                for j in subset:
                    templated_subset.append(max_candidate_line[j])

                # Now go through all the subsets of $line_length from $picked
                # Find the missing numbers from this subset
                missing_subset_numbers = []
                for j in range(1, max_number + 1):
                    if j not in templated_subset:
                        missing_subset_numbers.append(j)

                # Now build this up to lines of length $picked
                for missing_picked_subset in missing_picked_cover_template:

                    full_picked_line = templated_subset[:]
                    for j in missing_picked_subset:
                        full_picked_line.append(missing_subset_numbers[j])
                    full_picked_line.sort()

                    picked_csn = sequence_number(full_picked_line, max_number)
                    covered_picked_csns.add(picked_csn)

            f = open(file_name, "a")
            f.write(str(len(final_lines)) + ' (' + str(round((len(covered_length_csns)/lines_from_length) * 100, 2)) + '): '  + ' '.join([str(item) for item in max_candidate_line]) + "\n")
            f.close()

        if len(covered_length_csns) == lines_from_length:
            break;

    # Get the next line, only if this wasn't the last combination
    cur_line = next_combination(cur_line, max_number)

end_time = time.time() - start_time
print("--- %s seconds ---" %end_time )

f = open(file_name, "a")
f.write("*****\nTotal number of lines: " + str(len(final_lines)))
f.write("\nTime taken: " + str(end_time))
f.close()

summary(covered_picked_csns, lines_from_picked, final_lines)
