# -*- coding: utf-8 -*-

import h3m
from lxml import etree
import sys
#from guess_language import guessLanguage

map = h3m.extract(sys.argv[1])
#print guessLanguage(map["map_desc"])

print etree.tostring(map,pretty_print=True,xml_declaration=True,encoding="UTF-8")