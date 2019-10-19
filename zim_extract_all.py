# -*- coding: utf-8 -*-
import codecs
import re
import os
import argparse
from collections import Counter
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


# load the zimfile
zimfile = ZIMFile(args.zimfile, "utf-8")

# load the languages
with codecs.open(args.langfile, "rb", "utf-8") as f:
    languages = [line.strip() for line in f]

# create directories to store results
for language in languages:
    if not os.path.exists("./candidate_pages/" + language):
        os.makedirs("./candidate_pages/" + language)

count = 0
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
                if (
                    u">" + language + u"</h2>" in body
                    and (
                        u"Noun</h3>" in body
                        or u"Verb</h3>" in body
                        or u"Adjective</h3>" in body
                        or u"Pronoun</h3>" in body
                    )
                    and (
                        u"Conjugation" in body
                        or u"Declension" in body
                        or u"Inflection" in body
                    )
                ):
                    outf = codecs.open(
                        "./candidate_pages/"
                        + language
                        + "/candidate_"
                        + str(count)
                        + ".html",
                        "wb",
                        encoding="utf-8",
                    )
                    outf.write(body)
                    outf.close()
                    # update id
                count += 1
        except:
            print("BAD DATA", count)
        cblob += 1  # Update blob
    except IOError:
        cblob = 0  # reset blob
        cclust += 1  # update cluster
        if cclust >= zimfile.header_fields["clusterCount"]:  # no such cluster anymore
            OK = False
