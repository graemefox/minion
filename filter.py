#!/usr/bin/python -tt
import statistics
from statistics import mode
import argparse
parser = argparse.ArgumentParser(description='rough nanopore amplicon analysis')
parser.add_argument('-i','--input1', help='demultiplexed, fasta file', \
                    required=True)
args = parser.parse_args()
with open(args.input1, 'r') as input_file:
        ### get the most common start of sequence
        ## (rough and ready way to filter out reads in wrong orientation)
        list_of_seq_starts = list()
        for line in input_file:
            if not line.startswith(">"):
                list_of_seq_starts.append(line[:5])
        leader = mode(list_of_seq_starts)
input_file.close()
with open(args.input1, 'r') as input_file:
    with open(args.input1 + "_filtered", 'w') as forwards_reads:
        ## pull out forwards_reads
        for line2 in input_file:
            if line2.startswith(">"):
                header = line2
            elif line2.startswith(str(leader)):
                forwards_reads.write(header + line2)
