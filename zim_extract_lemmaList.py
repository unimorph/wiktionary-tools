# -*- coding: utf-8 -*-
import codecs
import re
import pandas as pd
from collections import Counter
import pickle
import time
import argparse
import numpy as np
from zimply import ZIMFile

# gather arguments
parser = argparse.ArgumentParser(
    description="Extract per-language lemma list from zim file."
)
parser.add_argument(
    "-zimfile", action="store", dest="zimfile", help="Location of ZIM file."
)
parser.add_argument(
    "-langfile", action="store", dest="langfile", help="List of languages."
)
args = parser.parse_args()

# regular expressions
lempat = r"<h1.*?>(.*?)</h1>"
locpat1 = r"</h2>.*?</h2>"
locpat2 = r"</h2>.*?</body>"
pospat = r">(.*?)</h3>"

# languages
with codecs.open(args.langfile, "rb", "utf-8") as f:
    languages = [line.strip() for line in f]

# create outputfiles
ofdict = {}
for language in languages:
    ofdict[language] = codecs.open(language + "_lemma_list_fast.txt", "wb", "utf-8")

count = 0
# times = []
zimfile = ZIMFile(args.zimfile, "utf-8")


cclust = 0
cblob = 0
OK = True
while OK:
    try:
        data = zimfile._read_blob(cclust, cblob)
        count += 1
        try:
            body = data.decode("utf-8")
            for language in languages:
                ln = language
                fout = ofdict[language]
                if language + u"</h2>" in body:
                    # this is probably a Spanish lemma
                    match = re.search(lempat, body, flags=re.U | re.DOTALL)
                    if match:
                        lemma = match.group(1)
                        # try to find the language block
                        match = re.search(ln + locpat1, body, flags=re.U | re.DOTALL)
                        if not match:
                            match = re.search(
                                ln + locpat2, body, flags=re.U | re.DOTALL
                            )
                        if match:
                            text = match.group()
                            matches = re.findall(pospat, text)
                            for x in matches:
                                fout.write(lemma + "\t" + x + "\n")
        except:
            print("BAD DATA", count)

        cblob += 1  # Update blob
    except IOError:
        cblob = 0  # reset blob
        cclust += 1  # update cluster
        if cclust >= zimfile.header_fields["clusterCount"]:  # no such cluster anymore
            OK = False


# clean up
for language in languages:
    ofdict[language].close()
fout.close()
