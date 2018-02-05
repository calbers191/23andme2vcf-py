#!/usr/bin/env python

import sys
from datetime import date

output_file = open(sys.argv[2], 'w')
output_file.write('##fileformat=VCFv4.2\n')
output_file.write('##fileDate=' + str(date.today()) + '\n')
output_file.write('##source=23andme2vcf.py https://github.com/calbers191/23andme2vcf-py\n')
output_file.write('##reference=23andme_reference_sequence.txt\n')
output_file.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
output_file.write('##CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tGENOTYPE\n')

with open(r'U:\23andme2vcf-py\23andme_reference_sequence.txt', 'r') as ref_sequence:
    ref_dict = {}
    for line_ref in ref_sequence:
        fields_ref = line_ref.strip().split('\t')
        chrom_ref = fields_ref[0]
        position_ref = fields_ref[1]
        ref_base = fields_ref[2]
        ref_dict[chrom_ref + '_' + position_ref] = ref_base

with open(sys.argv[1], 'r') as alt_sequence:
    for line_alt in alt_sequence:
        if not line_alt.startswith('#'):
            fields_alt = line_alt.strip().split('\t')
            rsid = fields_alt[0]
            chrom_alt = fields_alt[1]
            position_alt = fields_alt[2]
            call_1 = fields_alt[3][0]
            call_2 = fields_alt[3][1] if len(fields_alt[3]) > 1 else None

            no_calls = ['-', 'I', 'D']
            call_1_not_ref = False
            call_2_not_ref = False

            if call_1 not in no_calls and call_2 not in no_calls:
                    if (chrom_alt + '_' + position_alt) in ref_dict:
                        if call_2 is not None:
                            if call_1 != ref_dict[chrom_alt + '_' + position_alt]:
                                call_1_not_ref = True
                            if call_2 != ref_dict[chrom_alt + '_' + position_alt]:
                                call_2_not_ref = True
                        else:
                            if call_1 != ref_dict[chrom_alt + '_' + position_alt]:
                                call_1_not_ref = True

                        if call_1_not_ref is True and call_2_not_ref is True:
                            if call_1 == call_2:
                                output_file.write(
                                    'chr' + chrom_alt + '\t' + position_alt + '\t' + rsid + '\t' + ref_dict[
                                        chrom_alt + '_' + position_alt] + '\t' + call_1 + '\t.\t.\t.\tGT\t1/1\n')
                            else:
                                output_file.write(
                                    'chr' + chrom_alt + '\t' + position_alt + '\t' + rsid + '\t' + ref_dict[
                                        chrom_alt + '_' + position_alt] + '\t' + call_1 + ',' + call_2 + '\t.\t.\t.\tGT\t1/1\n')
                        elif call_1_not_ref is True:
                            output_file.write(
                                'chr' + chrom_alt + '\t' + position_alt + '\t' + rsid + '\t' + ref_dict[
                                    chrom_alt + '_' + position_alt] + '\t' + call_1 + '\t.\t.\t.\tGT\t0/1\n')
                        elif call_2_not_ref is True:
                            output_file.write(
                                'chr' + chrom_alt + '\t' + position_alt + '\t' + rsid + '\t' + ref_dict[
                                    chrom_alt + '_' + position_alt] + '\t' + call_2 + '\t.\t.\t.\tGT\t0/1\n')
                        else:
                            pass