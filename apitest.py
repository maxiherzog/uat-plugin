#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 15:28:56 2020

@author: maxi
"""

import pandas as pd
import overpy

resultstring = "[out:json][timeout:25];\n{{geocodeArea:Heidelberg}}->.searchArea;\n("

df=pd.read_csv('tagweights.csv', sep=':',header=0)
for i in range(0,len(df.values)-20):
    for x in range(2, 5):
        string = str(df.values[i][x])
        if not string == "nan":
            liststring = string.split(", ")
            for value in liststring:
                for pre in ["node", "way", "relation"]:
                    resultstring += "\t" + pre + '[\"' + df.columns[x] + '\"=\"' + value + '\"](area.searchArea);'

resultstring += "); \n out body;"
#print(resultstring)
api = overpy.Overpass()

result = api.query(resultstring)

print(result.get_ways())
