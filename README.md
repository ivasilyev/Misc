# Misc
The repository for my compact-sized tools.

>**WARNINGS/DISCLAIMERS**

> Every script is published for educational purposes only. Its code is presented "as is" and might not work in some cases. Make sure you have made all necessary changes in configuration parts and use help option!

##kegg_parser
This script allows to parse **MILLIONS** of KEGG entries within a very short time through [API](http://www.kegg.jp/kegg/docs/keggapi.html) using [pandas](http://pandas.pydata.org/) and [sh](https://amoffat.github.io/sh/) libraries from a single-column list into the table containing following columns: *ENTRY, NAME, DEFINITION, PATHWAY, MODULE, DISEASE, BRITE, DBLINKS, GENES*.
```
kegg_parser.py -i KEGG_list.txt -o KEGG_table.txt
```
##column_extractor
A simple multi-core tool for separation of one or few columns from table containing too large cells which cannot be processed by excel, pandas etc.
```
python column_extractor.py -i big_table.txt -d "\t" -c "0,3,5"
``` 
This will extract tab-delimited 1st, 4th and 6th column into a file "big_table_0,3,5.txt". 
##filechecker_empty
A tool for detection of zero-sized files within the specified directory containing large amount of files. However, it does not see file starting with special symbols, e.g. dots. 
```
filechecker_empty.py -i big_directory -o out.txt
```
##filechecker_exist
This tool retrieves two filelists from directories or text files and looks for missing filenames or text entries using [regular expressions](https://en.wikipedia.org/wiki/Regular_expression) for each fileset with both directions. 
```
filechecker_exist.py -a directory1 -b directory2 -z "(.*).txt" -y "(.*).not.quiet.txt" -o mask
```
Else:
```
filechecker_exist.py -a ls.log -b directory2 -z "(.*).txt" -y "(.*).not.quiet.txt" -o mask
```
Easily extract a list of missing (file)names:
```
grep MISSING mask_straight.txt | awk -v OFS='\t' {'print $1'} > to_do.txt
```
