#!/usr/bin/env python

import sys
from datetime import date


## Write header lines to VCF
output_file = open(sys.argv[2], 'w')
output_file.write('##fileformat=VCFv4.2\n')
output_file.write('##fileDate=' + str(date.today()) + '\n')
output_file.write('##source=23andme2vcf.py https://github.com/calbers191/23andme2vcf-py\n')
output_file.write('##reference=23andme_reference_sequence.txt\n')
output_file.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
output_file.write('##CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tGENOTYPE\n')


## Open reference sequence and store in dict, keyed by genomic coordinate
with open(r'23andme_reference_sequence.txt', 'r') as ref_sequence:
    ref_dict = {}
    for line_ref in ref_sequence:
        fields_ref = line_ref.strip().split('\t')
        chrom_ref = fields_ref[0]
        position_ref = fields_ref[1]
        genomic_coord_ref = chrom_ref + '-' + position_ref
        ref_base = fields_ref[2]
        ref_dict[genomic_coord_ref] = ref_base

## Open 23andme file provided as first command line argument.
with open(sys.argv[1], 'r') as alt_sequence_file:

    ## Process data line by line
    for line_alt in alt_sequence_file:

        ## Omit header
        if not line_alt.startswith('#'):

            ## Strip newline and split tab-separated fields
            fields_alt = line_alt.strip().split('\t')

            ## Set variables to corresponding fields
            rsid = fields_alt[0]
            chrom_alt = fields_alt[1]
            position_alt = fields_alt[2]
            genomic_coord_alt = chrom_alt + "-" + position_alt
            call_1 = fields_alt[3][0]
            call_2 = fields_alt[3][1] if len(fields_alt[3]) > 1 else None ## None if second call is missing

            ## Skip no calls, insertions, and deletions
            no_calls = ['-', 'I', 'D']

            ## Set mutation flags to false
            call_1_not_ref = False
            call_2_not_ref = False

            ## If both calls were made and not insertions or deletions
            if call_1 not in no_calls and call_2 not in no_calls:

                ## If genomic coordinate in alternate sequence matches genomic coordinate in reference
                if genomic_coord_alt in ref_dict:

                    ## If both calls were made
                    if call_2 is not None:

                        ## If alt doesn't match reference for either call, set corresponding flag to true
                        if call_1 != ref_dict[genomic_coord_alt]:
                            call_1_not_ref = True
                        if call_2 != ref_dict[genomic_coord_alt]:
                            call_2_not_ref = True

                    ## If second call wasn't made (X and Y in males, MT in all?)
                    else:

                        ## If alt doesn't match reference, set corresponding flag to true
                        if call_1 != ref_dict[genomic_coord_alt]:
                            call_1_not_ref = True

                    ## Write line of VCF based on results of mutation flags
                    ## If both flags are True, GT field written as 1/1
                    if call_1_not_ref is True and call_2_not_ref is True:

                        ## If both calls are identical, genotype is homozygous alt
                        if call_1 == call_2:
                            output_file.write(
                                'chr' + chrom_alt + '\t' + position_alt + '\t' + rsid + '\t' + ref_dict[
                                    genomic_coord_alt] + '\t' + call_1 + '\t.\t.\t.\tGT\t1/1\n')

                        ## If calls not identical, genotype is compound het and calls are comma separated
                        else:
                            output_file.write(
                                'chr' + chrom_alt + '\t' + position_alt + '\t' + rsid + '\t' + ref_dict[
                                    genomic_coord_alt] + '\t' + call_1 + ',' + call_2 + '\t.\t.\t.\tGT\t1/2\n')

                    ## If call 1 doesn't match reference, call 1 written to VCF
                    elif call_1_not_ref is True:
                        output_file.write(
                            'chr' + chrom_alt + '\t' + position_alt + '\t' + rsid + '\t' + ref_dict[
                                genomic_coord_alt] + '\t' + call_1 + '\t.\t.\t.\tGT\t0/1\n')

                    ## If call 2 doesn't match reference, call 2 written to VCF
                    elif call_2_not_ref is True:
                        output_file.write(
                            'chr' + chrom_alt + '\t' + position_alt + '\t' + rsid + '\t' + ref_dict[
                                genomic_coord_alt] + '\t' + call_2 + '\t.\t.\t.\tGT\t0/1\n')

output_file.close()