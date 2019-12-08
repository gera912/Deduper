#!/usr/bin/env python

# Program Header
# Course: Bi624
# Name:   Gera Perez
# Description: Our goal with this assignment is to remove all PCR duplicates (retain only a single copy of each read)
# from a sam file that has uniquely mapped reads,
#
# perez_Deduper.py
#
# Development Environment: Atom 1.38.2
# Version: Python 3.7.3
# Date:  12/07/2019
#################################################

# Imports module
import argparse
import re



# Creates an arguement passer
parser = argparse.ArgumentParser(description="A program for deduping")


# Adds arguemets by calling the arguement passer, for file name
parser.add_argument("-f", "--filename", help="specify the absolute file path", required=True)

# Adds arguemets by calling the arguement passer, for paired option
parser.add_argument("-p", "--paired", help="option designates file for paired end",required=False)

# Adds arguemets by calling the arguement passer, for file containing files
parser.add_argument("-u", "--umi", help="option designates file containing the list of UMIs", required=False)

# Parses arguemets through using the parse args method.
args = parser.parse_args()


# Try and except block to handle error if absolute file path is not given.
try:
    # regex to get the name of the sam file omitting '.sam'
    filename = re.search('.+/(.+).sam', args.filename)
    filename=filename.groups()

except AttributeError:
    # prints statement if absolute file path is not given
    print("Need file path")
    quit()

# if statement to print an error message and quit when given paired end.
if args.paired != None :
    print("No paired-end functionality yet")
    quit()

# Opens files to write, with _deduped.sam added to new file names.
deduped=open('%s_deduped.sam' % filename,"w")

# Opens files to write, with _duplicate.sam added to new file names.
duplicate=open('%s_duplicate.sam' % filename,"w")


# if statement to read UMI list
if args.umi== None :

    # if file is not given read the default UMI list.
    f=open("/home/gperez8/bgmp/projects/bgmp/gperez8/Bi624/Deduper/STL96.txt","r")

# else file is given then read the file
else : f=open(args.umi,"r")

# Stores the lines from UMI list to a variable.
lines=f.readlines()

# Creates an empty list for UMIs.
UMIs=[]

# A for loop that goes through each line.
for i in lines:

    # Strip and split each line, gets the 0th column (IMPORTANT!)
    x=i.strip().split('\t')[0]

     # Adds the value that was in the 0th column of each line into a list
    UMIs.append(x)

# Creates a function to check the strandness of each record by checking the bitwise flag
def check_bitwise(flags):
    '''Takes an integer and returns reverse if the bitwise flag is the reverse complement, else returns forward'''

    # Using if statements to check if flag equals 16 for reverse strand, else return forward
    if ((int(flags) & 16)==16):
        return "reverse"

    else: return "forward"


# Creates a function to account for softclipping in the plus strand
def soft_clip_plus(chromosome_location, CIGAR_string):
    '''Takes the chromosome location and Cigar string, returns the new chromosome location for the plus orientation'''

    # If statement that checks for an S character in the cigar string
    if CIGAR_string.find('S')== True:

        # If true slice the string before the S character.
        CIGAR_string=CIGAR_string[0:CIGAR_string.find('S')]

        # retuns difference of chromosome location and the softclipping
        return (int(chromosome_location)-int(CIGAR_string))

    # else if no S character return the chromosome location
    else: return chromosome_location

# Creates a function to account for softclipping in the minus strand
def soft_clip_minus(chromosome_location, CIGAR_string):
    '''Takes the chromosome location and Cigar string, returns the new chromosome location for the minus orientation'''

    # If statement that checks for an S character in the cigar string
    if CIGAR_string.find('S')== True:

        # If true slice the string after the S character.
        CIGAR_string=CIGAR_string[CIGAR_string.find('S')+1:]


    # finds all characters from the given list and splits them with numbers before it as a list.
    # Stores the result into a variable
    list_char=re.findall('[0-9]+[MIDNS]',CIGAR_string )

    # Creates an empty list
    new_list=[]

    # Creates a variabele
    soft_clip=0

    # For loop to check for specific charcters in the list
    for i in list_char:

        # Checks if I is NOT in the list
        if "I"  not in i:

            #if true gets numbers before I and appends to a new list
            new_list.append(int(i[:-1]))

        # Checks if S in the list
        if ("S") in i:

            # if true stores numbers before the S to a character and removes this item from new list
            soft_clip=int(i[:-1])+soft_clip
            new_list.pop()

    # returns the sum of the new list, softclipping and chromosome location
    return(sum(new_list)+soft_clip+ int(chromosome_location))

# Creates an empty dictionary
dict={}

# Opens a text file to read
with open(args.filename, 'r') as fh:


    # Creates an empty dictionary
    dedup_dict={}

    # for loop that goes through each line of sam read file.
    for line in fh:

        # if statement that checks if the @ is in the first index, checks header
        if line[0] == "@":

            # if true write the line to files
            deduped.write(line)
            duplicate.write(line)

        # if false split line through tabs as a list
        else:
            line=line.split()


            # Use regex to find the UMI from the 0th column of the sam file
            umi = re.search('.+:(.+)', line[0])
            umi=umi.groups()
            umi=umi[0]

            # Calls the function using the second column (bitwise FLAG) to get strandness
            strandness=check_bitwise(line[1])

            # If statement that checks for forward strandness
            if strandness == "forward":

                # if true, calls a function to get the plus position using the fourth column (POS field)
                # and sixth column (CIGAR field)
                position=soft_clip_plus(line[3],line[5])

            # if false calls a function to get the minus position using the 4th column (POS field)
            # and 6th column (CIGAR field)
            else: position=soft_clip_minus(line[3],line[5])

            # if statemnt that checks if UMI from record is in the UMI list
            if umi in UMIs:

                # if true, insert umi, chromosome, strandness and position into to tuple.
                key=(umi, line[2], strandness, position)

                # if the tuple in dictionary, then its a duplicate
                if key in dedup_dict:

                    # if true then write to the duplicate file
                    duplicate.write('\t'.join(line)+'\n')
                else:

                    # if false the set the tuple as a key and record as value for dictionary.
                    dedup_dict[key]=line

                    # write to the deduped file
                    deduped.write('\t'.join(line)+'\n')

deduped.close()
duplicate.close()
