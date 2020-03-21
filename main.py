#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:40:56 2020

@author: blobfishman
"""

import geopandas as gpd
import pandas as pd

grid = gpd.read_file(r"grid.shp")
points = gpd.read_file(r"points.shp")

# join points

dfsjoin = gpd.sjoin(grid, points, how="left", op='within')
dfpivot = pd.pivot_table(dfsjoin,index='id',columns='person-count',aggfunc={'id':len})
dfpivot.columns = dfpivot.columns.droplevel()

dfmerge = polys.merge(dfsjoin, how='left',on='id')

# join infrastructure

# join noise points
noise_points = gpd.read_file(r"noise-points.shp")

dfsjoin_noise = gpd.sjoin(grid, noise_points, how="left", op='within')
dfpivot_noise = pd.pivot_table(dfsjoin,index='id',columns='noise-person-count',aggfunc={'id':len})
dfpivot_noise.columns = dfpivot.columns.droplevel()

dfmerge_noise = polys.merge(dfsjoin_nosie, how='left',on='id')

# calculate value

