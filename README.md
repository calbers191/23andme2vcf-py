# 23andme2vcf-py
Python script for conversion of 23andme microarray data format to VCF.

I wrote this to accomodate the new v5 chip, which has ~638k SNPs and differs extensively from the previous versions. Reference sequence used is derived from GRCh37.

This conversion is inspired by and modeled after https://github.com/arrogantrobot/23andme2vcf. Please continue to use his script for v4 chip data and below.

Please let me know if there are any issues!
<hr>
<h2><strong>Usage:</strong></h2>

```
git clone https://github.com/calbers191/23andme2vcf-py.git

cd 23andme2vcf-py

./23andme2vcf.py /path/to/23andme_raw_data.txt /path/to/output.vcf
```
