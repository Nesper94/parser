#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  parser.py
#  
#  2020 Juan C. Arboleda R. <juan.arboleda2@udea.edu.co>

import csv

def main(ariba_out, ncbi_metadata):
    
    # Open files as csv dicts so that if these are very large files, they don't get loaded into memory at once
    data = csv.DictReader(ariba_out)
    ncbi_csv = csv.DictReader(ncbi_metadata)
    
    # Create list of accesions belonging to subclass CEPHALOSPORIN or CARBAPENEM
    ceph_carba = []

    for row in ncbi_csv:
        for key, val in row.items():
            if row['subclass'] == 'CEPHALOSPORIN' or row['subclass'] == 'CARBAPENEM':
                ceph_carba.append(row['refseq_nucleotide_accession'])
    
    # Print header
    print('sample name')

    for row in data:
        for key, value in row.items():
            
            # Get columns with suffix '.assembled' which value begins with 'yes'
            if key.endswith('.assembled') and value.startswith('yes'):
                
                if float(row[key.replace('.assembled','.ctg_cov')]) >= 10:
                    
                    if row[key.replace('.assembled','.ref_seq')].split('.',1)[1] in ceph_carba:
                        print(row['name'])
                        break  # If it meets the requirements, there is no need to keep looking this row

    return 0

if __name__ == '__main__':
    import sys, getopt
    
    # Documentation function
    def usage():
        print('Usage:',sys.argv[0],'-a <ariba output file> -n <ncbi metadata file>')
        print('      ',sys.argv[0],'[-h,--help]')
        print('')
        print('  -h, --help         show this help')
    
    # Raise exception if called with no arguments
    if len(sys.argv) == 1:
        usage()
        print('\nError: parser.py called with no arguments')
        sys.exit(1)
        
    # Interpret and collect arguments:

    short_opts = "ha:n:"
    long_opts = ["help"]

    try:
        arguments, values = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError as err:
        usage()
        print(sys.argv[0]+':', 'Error:', err)
        sys.exit(1)

    for opt, arg in arguments:
        
        if opt in ("-h", "--help"):
            usage(); sys.exit()
            
        elif opt == '-a':
            try:
                ariba_out = open(arg)
            except FileNotFoundError as err:
                usage()
                print(err)
                sys.exit(1)
        
        elif opt == '-n':
            try:
                ncbi_metadata = open(arg)
            except FileNotFoundError as err:
                usage()
                print(err)
                sys.exit(1)
        
    sys.exit(main(ariba_out, ncbi_metadata))
