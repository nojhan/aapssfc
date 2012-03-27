#encoding: utf-8

import sys
from urllib.request import urlopen
import re

def download( url ):
    with urlopen( url ) as page:
        while True:
            data = page.readline()
            if data:
                #print(data)
                yield data
            else:
                break

def grep( pattern, page ):
    for line in page:
        if re.match(pattern, line):
            yield line

def decode( strings ):
    for s in strings:
        yield s.decode("utf-8")
        
def format( strings ):
    for s in strings:
        res = s
        res = res.replace("'''","")
        res = res.replace("''","")
        res = re.sub(r'\[\[(\w*)\|\w*\]\]', r'\1', res)
        res = res.replace("[[","")
        res = res.replace("]]","")
        res = re.sub(r'{{-\w*-}}', r'', res)
        res = res.replace("\n","")
        yield res

term = sys.argv[1]
url="http://fr.wiktionary.org/w/api.php?format=xml&action=query&titles=%s&rvprop=content&prop=revisions&redirects=1"
match = "^:\s"

for d in grep( match, format( decode( download( url % term ) ) ) ):
    print(term,d)

