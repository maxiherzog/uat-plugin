#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:40:56 2020

@author: blobfishman
# """


import sys
import geopandas as gpd
import pandas as pd
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import numpy as np

def main():
    if len(sys.argv) != 6 :
        print("missing arguments. Usage:")
        print("python3 main.py GRID.shp INFRA_SCORES.shp POINTS.shp POINTS_BACKGROUND.shp SCORES_FINAL.shp")
        return

    grid = gpd.read_file(sys.argv[1])
    del grid['left']
    del grid['top']
    del grid['right']
    del grid['bottom']
    points = gpd.read_file(sys.argv[2])
    del points['field_1']
    del points['field_2']
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
    print("pivot")
    print(dfpivot)

    dfmerge = grid.merge(dfpivot, how='left',on='id')
    print("merge")
    print(dfmerge)

    # load infrastructure
    infra = gpd.read_file(sys.argv[3])
    print("infra")
    print(infra)
    # join noise points
    noise_points = gpd.read_file(sys.argv[4])

    dfsjoin_noise = gpd.sjoin(grid, noise_points, how="left", op='contains')
    dfpivot_noise = pd.pivot_table(dfsjoin_noise,index='id', aggfunc={'index_right':nanlen})

    dfmerge_noise = grid.merge(dfpivot_noise, how='left',on='id')
    print("merge noise")
    print(dfmerge_noise)

    # # calculate value
    val_points = dfmerge["index_right"]
    val_points_noise = dfmerge_noise["index_right"]
    y  = infra["infra_scor"]

    x = np.maximum(val_points-val_points_noise, np.ones(len(y)))
    # normalisieren
    val = x**y + x # Funktion

    # create return file
    dffinal = dfmerge_noise
    dffinal["index_right"] = val
    dffinal.columns=["id", "geometry", "val"]
    dffinal['pop'] = x
    dffinal['infra_score'] = y
    dffinal.to_file(driver="ESRI Shapefile", filename=sys.argv[5])
    print(dffinal)

main()
