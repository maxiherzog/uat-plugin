#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import overpy

# def getWeight(tags):
#     for poss_
#         string = str(df.columns[x])
        
#       pass  
df=pd.read_csv('tagweights.csv', sep=':',header=0)
resultstring = "[out:json][timeout:25];area[name=\"Heidelberg\"]->.searchArea;\n("

df=pd.read_csv('tagweights.csv', sep=':',header=0)
for i in range(0,len(df.values)-20):
    for x in range(2, 5):
        string = str(df.values[i][x])
        if not string == "nan":
            liststring = string.split(", ")
            for value in liststring:
                for pre in ["node", "way"]:
                    resultstring += "\t" + pre + '[\"' + df.columns[x] + '\"=\"' + value + '\"](area.searchArea);'

resultstring += "); out center;"
#print(resultstring)
api = overpy.Overpass()

result = api.query(resultstring)

print("Finished Query!")
print(len(result.nodes))


for n in result.get_nodes():
    print(n.tags)

for w in result.get_ways():
    print(w.get_nodes(resolve_missing=True))
