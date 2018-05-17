#!/usr/bin/python -tt

import argparse, subprocess
parser = argparse.ArgumentParser(description='blast clustered seqs')
parser.add_argument('-i','--input1', help='clustered minion file', \
                    required=True)
args = parser.parse_args()

with open(args.input1, 'r') as input_file:
    command="blastn -query " + args.input1 + " -db ~/ncbi/combined_nucl -task blastn -dust no -outfmt \"7 qseqid sseqid evalue bitscore pident qcovhsp sscinames staxids\" -perc_identity 75 -qcov_hsp_perc 75 -max_target_seqs 50 -num_threads 8 -out " + args.input1 + "_blast_output"
    subprocess.call(command, shell=True)
