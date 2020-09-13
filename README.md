# parser.py

Parser to identify samples that contain loci responsible for conferring cephalosporin or carbapenem resistance using an 
Ariba output file.

To use the script run `parser.py -a <ariba output file> -n <ncbi metadata file>`. The output consist in samples names 
meeting the requirements and will be written to stdout.

You can also get usage information by running `parser.py -h` or `parser.py --help`.
