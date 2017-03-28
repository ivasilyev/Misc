# Misc
The repository for my compact-sized tools.

>**WARNINGS/DISCLAIMERS**

> Every script is published for educational purposes only. Its code is presented "as is" and might not work in some cases. Make sure you have made all necessary changes in configuration parts and use help (*-h*) option!

## SingleBee_mp
This script is just a multi-core optimized [fork](https://github.com/ivasilyev/ThreeBees) of our existing project. It will take a single-column list of *csfasta* files with absolute paths, perform a single alignment (meant as "bee") it and collect the coverage statistics within the specified folder into *bp* or *pos* text files (short explanation can be found [here](https://github.com/ivasilyev/ThreeBees/blob/master/msbA.png)). **You must specify all necessary paths and references** in the configuration part. However, the script is sensitive to [keyboard interrupts](https://docs.python.org/2/library/exceptions.html), so **it is highly recommended to release the input** by the master command like:
```
nohup python SingleBee_mp.py -i weekly_csfasta.txt -d friday_dir -o alignment_for_weekend > /dev/null 2>&1 & echo $! > run.pid
```
You can generate the *csfasta* list with absolute paths by the following step:
```
 ls -d <absolute path to your dir starting with slash>/* | grep -i ".csfasta" > samples.txt
```
Feel free to use files from different sources.

## kegg_parser
This script allows to parse **MILLIONS** of KEGG Orthology DB (*KXXXXX*) entries within a very short time through [API](http://www.kegg.jp/kegg/docs/keggapi.html) using [pandas](http://pandas.pydata.org/) and [sh](https://amoffat.github.io/sh/) libraries from a single-column list into the table containing following columns: *ENTRY, NAME, DEFINITION, PATHWAY, MODULE, DISEASE, BRITE, DBLINKS, GENES*.
```
kegg_parser.py -i KEGG_KO_list.txt -o KEGG_table.txt
```

## kegg_compounds2orthologs
Similar to the previous one, but performs a search by KEGG DB Compound DB IDs (*CXXXXX*) and dumps results in the following columns: *KEGG Compound, Synonyms, KEGG Enzymes, KEGG orthologs*.
```
kegg_compounds2orthologs.py -i KEGG_CD_list.txt -o KEGG_CD_with_KO_table.txt
```

## column_extractor
A simple multi-core tool for separation of one or few columns from a table containing too large cells with special symbols, e.g. spaces, which cannot be processed by Excel, *pandas, awk* etc.
```
column_extractor.py -i big_table.txt -d "\t" -c "0,3,5"
``` 
This will extract tab-delimited (by default) 1st, 4th and 6th columns into a file *big_table_columns_0,3,5.txt* (zero-based). 

## make_table_great_again
A combining tool to merge all files from table without a header with sample names and related paths with header-supplied existing table by the specified index column into large dataframe using [pandas](http://pandas.pydata.org/) library.
```
make_table_great_again.py -i sampledata.txt -t annotation.txt -c index_id -o combined_samples
```
This will produce *annotation_merged_by_index_id_raw_data.txt* and *annotation_merged_by_index_id_percentage.txt* into the *combined_samples* directory.

##percentage_plot
This script allows to visualize a specified part of the existing dataframe through a heatmap. As an option, the percentage may be calculated from the given external data containing tab-delimited sample name and pre-calculated total sum. The required packages are [pandas](http://pandas.pydata.org/), [matplotlib](http://matplotlib.org/) and [seaborn](https://seaborn.pydata.org/).
```
python3 percentage_plot.py -i sampledata.txt -t dataframe_with_header.txt -s sum.txt -c index_id -o heatmap_1

```
Like the previous, resulting it dataframes with raw and percentage data supplied with the heatmaps would be created created into the *heatmap_1* directory.

## filechecker_empty
A tool for detection of zero-sized files within the specified directory containing pretty large amount of files. However, it does not see files starting with special symbols, e.g. dots. 
```
filechecker_empty.py -i big_directory -o out.txt
```

## filechecker_exist
This tool retrieves two filelists from existing directories or text files and looks for missing filenames or text entries using [regular expressions](https://en.wikipedia.org/wiki/Regular_expression) for each fileset with both directions. 
```
filechecker_exist.py -a directory1 -b directory2 -z "(.*).txt" -y "(.*).not.quiet.txt" -o mask
```
Else:
```
filechecker_exist.py -a ls.log -b directory2 -z "(.*).txt" -y "(.*).not.quiet.txt" -o mask
```
Easily extract the list of missing (file)names:
```
grep MISSING mask_straight.txt | awk -v OFS='\t' {'print $1'} > to_do.txt
```

## regex_slicer
A script for [regex](https://en.wikipedia.org/wiki/Regular_expression)-based file chopping using [numpy](http://www.numpy.org/) package:
```
regex_slicer.py -i reference.fasta -n 3 -p ">"
```
It will cut *reference.fasta* to files *reference_chunk_1.fasta, reference_chunk_2.fasta, reference_chunk_3.fasta.* By default, the splitting expression is *"\n"*. **Note that all empty strings will be removed.**