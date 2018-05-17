#!/usr/bin/python -tt

import argparse, subprocess
parser = argparse.ArgumentParser(description='blast clustered seqs')
parser.add_argument('-i','--input1', help='clustered minion file', \
                    required=True)
args = parser.parse_args()

with open(args.input1, 'r') as input_file:
    command="blastn -query " + args.input1 + " -db ~/ncbi/combined_nucl -task blastn -dust no -outfmt \"7 qseqid sseqid evalue bitscore pident qcovhsp sscinames staxids\" -perc_identity 75 -qcov_hsp_perc 75 -max_target_seqs 5 -num_threads 8 -out " + args.input1 + "_blast_output"
    subprocess.call(command, shell=True)

blast_results = list()
unique_species = set()
blast_results.append('\t'.join(["Species", "NCBI_ID", "E-Score", "%_Identity", "%_Coverage"]))
with open(args.input1 + "_blast_output", 'r') as blast_output:
    for line in blast_output:
        new_result = 0
        if line.rstrip("\n") == "# BLASTN 2.6.0+":
            new_result = 1
            for i in range(0, 3):
                line = blast_output.next()
            if line.rstrip("\n") == "# 0 hits found":
                line = blast_output.next()
            else:
                line = blast_output.next()
                line = blast_output.next()
                    # parse the data
                ncbi_id = line.split("\t")[1]

                blast_results.append('\t'.join([line.split("\t")[6],
                                            ncbi_id.split("|")[1],
                                            line.split("\t")[2],
                                            line.split("\t")[4],
                                            line.split("\t")[5]]) + "\n")
                unique_species.add(line.split("\t")[6])

### go through blast data and spit out the best result (or results)
print(blast_results[0])
unique_species = list(unique_species)
for n in range(len(unique_species)):
    check = 0
    for line in blast_results:
        if not check == 1:
            if unique_species[n] == line.split("\t")[0]:
                check = 1
                print(line)
                if n < len(unique_species)-1:
                    n = n + 1
                else:
                    continue
        else:
            break
