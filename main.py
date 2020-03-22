#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:40:56 2020

@author: blobfishman
"""

import geopandas as gpd
import pandas as pd
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

grid = gpd.read_file(r"gitter_wgs84.shp")
del grid['left']
del grid['top']
del grid['right']
del grid['bottom']
points = gpd.read_file(r"random_points.shp")
del points['field_1']
del points['field_2']
# points.rename(columns={'id': 'points_id'})

# join points

dfsjoin = gpd.sjoin(grid, points, how="left", op='contains')
dfpivot = pd.pivot_table(dfsjoin,index='id', aggfunc=len)
del dfpivot['geometry']
# dfpivot.columns = dfpivot.columns.droplevel()
print("points")
print(points)
print("join")
print(dfsjoin)
print("pivot")
print(dfpivot)

dfmerge = grid.merge(dfpivot, how='left',on='id')
pd.set_option('display.max_rows', 7000)
print("merge")
print(dfmerge)

# join infrastructure

# join noise points
noise_points = gpd.read_file(r"time_0_points.shp")

dfsjoin_noise = gpd.sjoin(grid, noise_points, how="left", op='contains')
dfpivot_noise = pd.pivot_table(dfsjoin,index='id',aggfunc=len)
# dfpivot_noise.columns = dfpivot.columns.droplevel()

dfmerge_noise = grid.merge(dfpivot_noise, how='left',on='id')

# calculate value

