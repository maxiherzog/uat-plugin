#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:40:56 2020

@author: blobfishman
# """


import geopandas as gpd
import pandas as pd
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import numpy as np

grid = gpd.read_file(r"gitter_wgs84.shp")
del grid['left']
del grid['top']
del grid['right']
del grid['bottom']
points = gpd.read_file(r"random_points.shp")
del points['field_1']
del points['field_2']
# points.rename(columns={'id': 'points_id'})
print("points")
print(points)
# join points

dfsjoin = gpd.sjoin(grid, points, how="left", op='contains')
print("join")
print(dfsjoin)

# Super ekliges Workaround:
# Zählfunktion ignoritert Geometry und nan
# TODO pivot_table fixen
def nanlen(lst):
    ct = 0
    for l in lst:
        if str(type(l)) == "<class 'float'>":
            if  not str(l) == "nan":
                #print(l)
                ct+=1
    return ct
# dropna macht nichts?
dfpivot = pd.pivot_table(dfsjoin,index='id', aggfunc={'index_right':nanlen}, dropna=True)
#dfpivot.columns = dfpivot.columns.droplevel()
#del dfpivot['geometry']
print("pivot")
print(dfpivot)
# dfpivot.columns = dfpivot.columns.droplevel()

dfmerge = grid.merge(dfpivot, how='left',on='id')
#pd.set_option('display.max_rows', 7000)
print("merge")
print(dfmerge)

# join infrastructure
infra = gpd.read_file("infra_scores.shp")
print("infra")
print(infra)
# join noise points
noise_points = gpd.read_file(r"time_0_points.shp")

dfsjoin_noise = gpd.sjoin(grid, noise_points, how="left", op='contains')
dfpivot_noise = pd.pivot_table(dfsjoin_noise,index='id', aggfunc={'index_right':nanlen})
# dfpivot_noise.columns = dfpivot.columns.droplevel()

dfmerge_noise = grid.merge(dfpivot_noise, how='left',on='id')
print("merge noise")
print(dfmerge_noise)

# # calculate value
val_points = dfmerge["index_right"]
val_points_noise = dfmerge_noise["index_right"]
y  = infra["infra_scor"]

x = np.maximum(val_points-val_points_noise, np.ones(len(y)))
# normalisieren
# x = x/np.max(x)
val = x**y + x # Funktion
# val = val/np.max(val)
pd.set_option('display.max_rows', 6500)

# create return file
dffinal = dfmerge_noise
dffinal["index_right"] = val
dffinal.columns=["id", "geometry", "val"]
dffinal.to_file(driver="ESRI Shapefile", filename='scores.shp')
print(val)
