# wiktionary-tools
Wiktionary scraping, parsing, and annotation tools from the UniMorph Project

## Warning

These scripts are provided for reference purposes. Support is not guaranteed. 

## Prerequisites

1. [ZIMply](https://pypi.org/project/zimply/) (requires Python3)
2. [Wiktionary ZIM archive](https://download.kiwix.org/zim/wiktionary/)
3. [(OPTIONAL) Sample raw and annotated table templates](https://github.com/unimorph/wiktionary-annotations)

## Usage

Extract a list of lemma words from Wiktionary ZIM archive (*nopic* files preferred for smaller file sizes) for each language listed in languages file (one per line). Each lemma is associated with a possible part of speech. Results appear as ```LANGUAGE_lemma_list_fast.txt``` files.

```bash
python zim_extract_lemmaList.py -zimfile wiktionary_en_all_nopic_2017-08.zim -langfile languages.txt
```

Extract html candidate pages form Wiktionary ZIM archive for languages listed in languages file (one per line). These pages are likely to contain morphological inflection tables. Results appear in a ```candidate_pages``` directory.

```bash
python zim_extract_all.py -zimfile wiktionary_en_all_nopic_2017-08.zim -langfile languages.txt
```

Create annotation templates from candidate pages. This generates ```raw_tables``` and ```annotated_tables``` directories.

```bash
python extract_example_tables.py -candidates_dir candidate_pages
```

After annotation (see guide below, and examples in [wiktionary-annotation](https://github.com/unimorph/wiktionary-annotations) repo for reference), create morphologically annotated wordlists for all lemmas in each language. Annotation directory must contain both ```raw_tables``` and ```annotated_tables``` sub-directories. Results are generated in a ```tabular_results``` directory in the form of ```LANGUAGE_tabular_paradigms.txt``` files. ```fixParadigms.py``` removes paradigms that generated exceptions during parsing, resulting in ```LANGUAGE_tabular_paradigms_norm.txt``` output.

```bash
python extract_tabular_data.py -candidates_dir candidate_pages -annotation_dir . -language Ukrainian
python fixParadigms.py -language Ukrainian
```


## Annotation Guide

1. Select a language and table to annotate from the *raw* tables directory. For example, ```raw_tables/Adyghe/N_001427_(6,3)_example.csv```

    The file names follow the convention: ```POS_LEMMACOUNT_SHAPE_example.csv```

    For example, looking at ```N_001427_(6,3)_example.csv```:
    * This is a table type associated with noun lemmas.
    * There are 1427 lemmas that share this table template.
    * The shape of the extracted table is 6 rows by 3 columns.

2. Copy the selected file to the *annotated* tables directory. This will be the version that you will annotate. For example, ```annotated_tables/Adyghe/N_001427_(6,3)_example.csv```

    __DO NOT MODIFY THE ORIGINAL RAW FILE__. The annotation pipeline relies on finding the differences between the unannotated and annotated files.

3. Open the copy in an editor. You will be greeted with a table of forms and grammatical descriptors as shown below.

    __AVOID USING EXCEL. IT MANGLES UNICODE CHARACTERS BY DEFAULT. LIBREOFFICE IS RECOMMENDED INSTEAD.__
    
    ![Example raw table.](/images/raw_table_example.png "Example raw table.")
    
4. In order to cleanly extract all the inflected forms associated with a lemma with a particular table template, you just need to replace each inflected cell in the example template file with the correct UniMorph tags that correspond to it. It can help to look up the example lemma in Wiktionary online as additional reference. See below for an example.

    __DO NOT MODIFY ANY OF THE TABLE CELLS THAT DON’T CORRESPOND TO INFLECTED FORMS__ (e.g., any cells that correspond to grammatical descriptors like nominative, genitive, plural, etc.).
    
    ![Example annotated table.](/images/annotated_table_example.png "Example annotated table.")
    
5. Save the modified file, and that’s it!

Here are some additional guidelines.

* Avoid adding labels for innate lexical properties of words, especially if these aren’t __EXPLICITLY__ written somewhere in the table you are annotating. These may include lexical gender or animacy for nouns, or aspect for Slavic verb systems. Focus instead on non-innate inflectional features that are marked in the table (e.g., noun case, verb tense, aspect for non-Slavic verbs).

    __POSSIBLE EXCEPTION__: IF a lexical property __IS__ marked in the table you are annotating, __AND__ you are reasonably sure that the same table structure isn’t shared by words with different lexical properties, it probably doesn’t hurt to include the lexical property if UniMorph has a tag for it.

* If you spot any cells that are wrong or shouldn't be extracted because they don't involve inflected forms of the correct part of speech, simply don't assign any UniMorph tags to them, and leave them as is. This could mean ignoring entire files, but that's fine.

* Many table templates have a low count (~1), meaning only one lemma has that table type associated with it. It's up to you if you think it's worth annotating those.
