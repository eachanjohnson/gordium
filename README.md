# gordium.py

Cutting the Gordian knot of un-demultiplexed Illumina FASTQ files.

Fast demultiplexing of Illumina FASTQ files using Python.

## Usage
```
Usage:  gordium.py [-h|-v]
        gordium.py -d <demultiplex-params> (-r <read-files>...) (-b <barcode-files>...)

Options:
--help, -h                                              Show this page and exit
--version, -v                                           Show version number and exit
-d                                                      TSV of barcode values and filenames
-r <read-files>..., --reads <read-files>...             List of files containing reads
-b <barcode-files>..., --barcodes <barcode-files>...    List of files containing barcodes to be matched
```

## Example files
### `-d <demultiplex-params>`
`$ more 1_demultiplexing_library_params.txt`
```
OUTPUT_PREFIX	BARCODE_1	BARCODE_2
1_B8GFH.1.unmatched	N	N
1_B8GFH.1.TATCCTCT_GGACTCCT.unmapped	GGACTCCT	TATCCTCT
1_B8GFH.1.TATCCTCT_TAGGCATG.unmapped	TAGGCATG	TATCCTCT
1_B8GFH.1.AGAGTAGA_TAAGGCGA.unmapped	TAAGGCGA	AGAGTAGA
1_B8GFH.1.AGAGTAGA_CGTACTAG.unmapped	CGTACTAG	AGAGTAGA
1_B8GFH.1.AGAGTAGA_AGGCAGAA.unmapped	AGGCAGAA	AGAGTAGA
1_B8GFH.1.AGAGTAGA_TCCTGAGC.unmapped	TCCTGAGC	AGAGTAGA
1_B8GFH.1.AGAGTAGA_GGACTCCT.unmapped	GGACTCCT	AGAGTAGA
1_B8GFH.1.AGAGTAGA_TAGGCATG.unmapped	TAGGCATG	AGAGTAGA
1_B8GFH.1.TATCCTCT_TAAGGCGA.unmapped	TAAGGCGA	TATCCTCT
1_B8GFH.1.TATCCTCT_CGTACTAG.unmapped	CGTACTAG	TATCCTCT
1_B8GFH.1.TATCCTCT_AGGCAGAA.unmapped	AGGCAGAA	TATCCTCT
1_B8GFH.1.TATCCTCT_TCCTGAGC.unmapped	TCCTGAGC	TATCCTCT
```

### __`-r <read-files>...`__

`$ head -n 8 1_B8GFH.1.1.fastq`
```
@SL-MAK:B8GFH170608:B8GFH:1:1101:10000:12790 1:N:0:
GCCCTCGCAGTGATTAGGCAGCACCCGGTAATGGTGTTCTTCGCGCTGTCGCCGGTACTCGCCGCATTGGGTGTCATGTGGTGGCTAGCCGGTGCTGGATGGGCTATCGTCGCGGCCCTGGTGCTGGTGGTCGTCGGCGGAGCCATGATC
+
DDDCCDDDDCCFGGGGGGGGGGHHHGGGEGGHGHFGHGHHHHHGGGGGFHGHGGGGGGHHGGGGGGGGHHHEGGHHHHHHHHGG0FHHHHGGDGGHHHHHHGHHHHHGGHHGGGGCGGHHHHHHHHHHHGFHGGGGGGGGFGGGGGGGGF
@SL-MAK:B8GFH170608:B8GFH:1:1101:10000:13684 1:N:0:
GTTCAGGCTTCACCACAGTGTGGAACGCGGTCGTCTCCGAACTTAACGGCGACCCTAAGGTTGACGACGGACCCAGCAGTGATGCTAATCTCAGCGCTCCGCTGACCCCTCAGCAAAGGGCTTGGCTCAATCTCGTCCAGCCATTGACCA
+
ABCCBFFFFFFFGGGGGGGGGGGHHGGGGGGGGGGHHHEEGGHHFHHGGGGCGGGHHHGHHHHHHGGFGGGGFGGFHHHHHFHHHHHHHHHHHHHGGGGGGGGGGHHHGGGHHHHHHHGGGGHGGHHHHHHHHHGGGGGHHGHHHGGHHB
```

`$ head -n 8 1_B8GFH.1.2.fastq`
```
@SL-MAK:B8GFH170608:B8GFH:1:1101:10000:12790 2:N:0:
GACGATCATGGCTCCGCCGACGACCACCAGCACCAGGGCCGCGACGATAGCCCATCCAGCACCGGCTAGCCACCACATGACACCCAATGCGGCGAGTACCGGCGACAGCGCGAAGAACACCATTACCGGGTGCTGCCTAATCACTGCGAG
+
A3ABABBAFFFFGGGGGGGEFGGGGGHGHHGHHHHHGGGGGGGGGGGGGGGHHHHHHHHHHHHGGGGGAGFHHHHHHHHHHHHGGGHHHHGGGGGGGHHHGGGCGGFFGGGGGGGGGGGGGGGGGGGGGFDFFFFFFFFFFFFFFFFFFF
@SL-MAK:B8GFH170608:B8GFH:1:1101:10000:13684 2:N:0:
CCCGGGAACAACCGTTGGGCATAGTTGCCTGCCGCGTGTAGCAGGTGTGTCTTGCCGAGACCGGACTCGCCCCAGATGAACAGGGGGTTGTAAGCGCGGGCGGGTGCTTCTGCGATCGCCAAGGCGGCGGCGTGCGCGAACCGGTTGGAG
+
AAAA@?@1ACFACEEGEAEG00AG2GHGCFGHHGGGEGEFHG2FACCFEGFHGGFHG/EEEEGEE/EFEGGGGGGAGFDGGGCGFEGGGCADGHHGGGGCCGGC?AFFFGGBF@@FGGGGGGGEE@@@?<@@??F-@@?@?<-@=99@/F
```

### __`-b <barcode-files>...`__

`$ head -n 8 1_B8GFH.1.barcode_1.fastq`
```
@SL-MAK:B8GFH170608:B8GFH:1:1101:10000:12790 :N:0:
CGTACTAG
+
BAABBCFF
@SL-MAK:B8GFH170608:B8GFH:1:1101:10000:13684 :N:0:
AGGCAGAA
+
CCCCCCCF
```

`$ head -n 8 1_B8GFH.1.barcode_2.fastq`
```
@SL-MAK:B8GFH170608:B8GFH:1:1101:10000:12790 :N:0:
TATCCTCT
+
CBCCCFFF
@SL-MAK:B8GFH170608:B8GFH:1:1101:10000:13684 :N:0:
TATCCTCT
+
AAA3AFFF
```



