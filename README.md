# Misc
The repository for my compact-sized tools.

>**WARNINGS/DISCLAIMERS**

> Every script is published for educational purposes only. Its code is presented "as is" and might not work in some cases. Make sure you have made all necessary changes in configuration parts and use help (*-h*) option!

## afm2ped
This script converts Thermo Fisher Affymetrix™ output data from single or multiple files into single PED file:
```
afm2ped.py -a DF_2017071101_ssp_bestrec_ext.txt DF_2017071401_ssp_bestrec_ext.txt -p ped0.txt -s sampledata.txt -o output.ped
```

## column_extractor
A simple multi-core tool for separation of one or few columns from a table containing too large cells with special symbols, e.g. spaces, which cannot be processed by Excel, *pandas, awk* etc.
```
column_extractor.py -i big_table.txt -d "\t" -c "0,3,5"
```
This would extract tab-delimited (by default) 1st, 4th and 6th columns into a file *big_table_columns_0,3,5.txt* (zero-based).

## humann2_wrapper
A wrapper for parallelizing [HUMAnN2](https://bitbucket.org/biobakery/humann2/wiki/Home) pipeline. May use custom input string.
```
humann2_wrapper.py -i ls.log -o humann2_crohn -c 10
```
This action allows to create 10 HUMAnN2 pipelines in time using absolute paths stored in the *ls.log* file.

## kegg_parser
This script allows to parse **MILLIONS** of KEGG Orthology DB (*KXXXXX*) entries within a very short time through [API](http://www.kegg.jp/kegg/docs/keggapi.html) using [pandas](http://pandas.pydata.org/) and [sh](https://amoffat.github.io/sh/) libraries from a single-column list into the table containing following columns: *ENTRY, NAME, DEFINITION, PATHWAY, MODULE, DISEASE, BRITE, DBLINKS, GENES*.
```
kegg_parser.py -i KEGG_KO_list.txt -o KEGG_table.txt
```

## kegg_products2orthologs
Similar to the previous one, but performs a search by KEGG DB Compound DB IDs (*CXXXXX*) and dumps results in the following columns: *KEGG Compound, Synonyms, KEGG Enzymes, KEGG orthologs*.
```
kegg_products2orthologs.py -i KEGG_CD_list.txt -o KEGG_CD_with_KO_table.txt
```

## column_extractor
A simple multi-core tool for separation of one or few columns from a table containing too large cells with special symbols, e.g. spaces, which cannot be processed by Excel, *pandas, awk* etc.
```
column_extractor.py -i big_table.txt -d "\t" -c "0,3,5"
```
This will extract tab-delimited (by default) 1st, 4th and 6th columns into a file *big_table_columns_0,3,5.txt* (zero-based).

## table_grep
Opposite to the previous, this tool allows to make a subtable containing special substring from the bigger table using [sh](https://pypi.python.org/pypi/sh) library.
```
table_grep.py -i big_table.txt -k new_keyword -o key_table.txt
```

## keywords2fasta
Given a header keywords list, performs a positive or negative headers and sequences extraction.


## sum_count
Given a table and zero-based columns inexes list, returns column name and sum of values for each column. Requires [pandas](http://pandas.pydata.org/) package.
```
sum_count.py -i input_table -c 1,2,4 -o output_table
```

## percentage_plot
This script allows to visualize a specified part of the existing dataframe through a heatmap. As an option, the percentage may be calculated from the given external data containing tab-delimited sample name and pre-calculated total sum. The required packages are [pandas](http://pandas.pydata.org/), [matplotlib](http://matplotlib.org/) and [seaborn](https://seaborn.pydata.org/).
```
python3 percentage_plot.py -i sampledata.txt -t dataframe_with_header.txt -s sum.txt -c index_id -o heatmap_1 -f 0.05
```
Like the previous, resulting it, dataframes with raw and percentage data supplied with the heatmaps containing 0.05x-scaled axis will be created inside the *heatmap_1* directory.

## psqldb2table
Given a PostgreSQL table address, exports it to text table.

## regex_slicer
A script for [regex](https://en.wikipedia.org/wiki/Regular_expression)-based file chopping using [numpy](http://www.numpy.org/) package:
```
regex_slicer.py -i reference.fasta -n 3 -p ">"
```
It will cut *reference.fasta* to files *reference_chunk_1.fasta, reference_chunk_2.fasta, reference_chunk_3.fasta.* By default, the splitting expression is *"\n"*. **Note that all empty strings will be removed.**

## table2psqldb
Given a PostgreSQL table address and text table, uploads the text table as SQL table. Also provides recognition of some data types.
