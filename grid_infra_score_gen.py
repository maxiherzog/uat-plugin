 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 15:28:56 2020
@author: maxi
"""

import pandas as pd
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from shapely.geometry import Polygon
import numpy as np
import overpy
import sys
import time

def main():
    if len(sys.argv) != 4:
        print("missing arguments. Usage:")
        print("python3 grid_infra_score_gen.py GRID.shp TAG_WEIGHTS.csv INFRA_SCORES.shp")
        return

    start_time = time.time()

    print("Loading Grid Shape File at " + sys.argv[1])

    try:
        grid = gpd.read_file(sys.argv[1])
        minx, miny, maxx, maxy = grid.geometry.total_bounds
        rnd = 4
        bb = str(round(miny,rnd)) + "," + str(round(minx,rnd)) + "," + str(round(maxy,rnd)) + "," + str(round(maxx,rnd))
        print("Found boundary box (", bb,  ")")
        try:
            del grid['left']
            del grid['top']
            del grid['bottom']
            del grid['right']
        except:
            pass
    except:
        print("Grid shape file could not be located or is in the wrong format. Do you also have the .shx and .dbf files in the same directory?. Aborting..")
        return

    print("Loading Tagweights at " + sys.argv[2])
    try:
        df=pd.read_csv(sys.argv[2], sep=':',header=0)
    except:
        print("Tagweights file could not be located. Aborting..")
        return


    # Hier Timeout ändern, falls keine Rückgabe!
    #resultstring = "[out:json][timeout:200];area[name=\"Heidelberg\"]->.searchArea;\n("


    resultstring = "[out:json][timeout:200];\n("
    crs = {'init': 'epsg:4326'} #4326
    #df=pd.read_csv('tagweights.csv', sep=':',header=0)
    dict = {}
    print("Collecting dict: ")
    for i in range(0,len(df.values)):
        for x in range(2, 5):
            string = str(df.values[i][x])
            if not string == "nan":
                liststring = string.split(", ")
                for value in liststring:
                    dict[value] = df.values[i][6]
                    print(value + " [" + str(df.values[i][6]) + "]")
                    for pre in ["node", "way"]:
                        resultstring += "\t" + pre + '[\"' + df.columns[x] + '\"=\"' + value + '\"](' + bb +');'

    resultstring += ");out; >; out;"
    #print(resultstring)
    api = overpy.Overpass()
    #print(dict["cafe"])
    print("Starting query. This may take a while(<200s)...")
    try:
        result = api.query(resultstring)
    except:
        print("Query failed. Either there is no internet connection or the query timed out. Aborting..")
        return


    print("Finished query!")
    print(str(len(result.nodes)) + " nodes found.(also containing the unzipped ways)")
    print(str(len(result.ways )) + " ways found.")

    if len(result.nodes) == 0 and len(result.ways) == 0:
        print("Query returned no results. Maybe it took to long. Aborting...")
        return
    #print(dict['bakery'])

    def findWeight(tags):
        for poss_key in df.columns[2:5]:
            if poss_key in tags:
                if tags[poss_key] in dict.keys():
                    return dict[tags[poss_key]]
        return 0


    COLNAMES = ["point_id", "lon", "lat", "infra_score"]
    nodedf = pd.DataFrame(columns = COLNAMES)

    print("Analyzing nodes...")
    # Nodes
    nodes = result.get_nodes()
    for i in range(len(nodes)):

        n = nodes[i]
        #print(n.tags)
        weight = findWeight(n.tags)
        nodedf.loc[i] = [n.id, n.lon, n.lat, weight]
        #print(n.id, n.lon, n.lat, weight)

    #print(df)

    geometry = [Point(xy) for xy in zip(nodedf.lon, nodedf.lat)]

    geo_df = GeoDataFrame(nodedf, crs=crs, geometry=geometry)
    del geo_df['lat']
    del geo_df['lon']
    del geo_df['point_id']

    #print("Eingangs- Grid: ")
    #print(grid)

    dfsjoin = gpd.sjoin(grid, geo_df, how="left", op='contains')
    dfpivot = pd.pivot_table(dfsjoin, index="id", aggfunc={'infra_score': np.sum})
    # dfpivot.columns = dfpivot.columns.droplevel()

    #print(dfpivot)

    dfgridnew = grid.merge(dfpivot, how='left', on="id")
    #dfgridnew.drop(["left", "top", "right", "bottom"], axis=1)
    #print("Gemergtes Grid: ")
    #print(dfgridnew)

    #id, infra_wert, geometry

    #Berechnung der Infrastrukturwerte der ways
    print("Analyzing ways(e.g. building outlines)...")
    ways = result.get_ways()
    weight_list = [0] * len(ways) * 200
    meta_geo = [None] * len(ways) * 200
    ct = 0
    for i in range(len(ways)):
        w = ways[i]
        #print(w.tags)

        nodes = w.get_nodes(resolve_missing=False)
        N = len(nodes)
        lat_list = [0] * N
        lon_list = [0] * N

        # Scheint nicht zu funktionieren -> siehe Discord
        for j in range(N):
            n = nodes[j]
            lat_list[j] = n.lat
            lon_list[j] = n.lon


            #print(n.id, n.lon, n.lat,weight)
        try:
            poly_geo = Polygon(zip(lon_list, lat_list))
            meta_geo[ct] = poly_geo
            ct+=1
            weight_list[ct] = findWeight(w.tags)
        except:
            print("WARNING: Invalid way-shape fount @id=", w.id, "i=", i , " ignoring...")
            pass

        #Alternative Eckpunkte mit Bewertung/Anzahl der Eckpunkte
        # weight_w = findWeight(w.tags)
        # for j in range(N):
        #     n = nodes[j]
        #     lat_list[j] = n.lat
        #     lon_list[j] = n.lon
        #
        #     point_geo = Point(n.lat, n.lon)
        #     meta_geo[ct] = point_geo
        #     weight_list[ct] = weight_w/N
        #     ct+=1

    #arrs zuschneiden
    weight_list = weight_list[:ct]
    meta_geo = meta_geo[:ct]

    weight_df = pd.DataFrame(weight_list, columns=["infra_score"])

    poly_df = GeoDataFrame(weight_df, crs=crs, geometry=meta_geo)
    # print("infra_sco")
    # print(weight_df)

    polysjoin = gpd.sjoin(grid, poly_df, how="left", op='contains')
    polypivot = pd.pivot_table(polysjoin, index="id", aggfunc={'infra_score': np.sum})
    # dfpivot.columns = dfpivot.columns.droplevel()

    finalgrid = grid.merge(polypivot, how='left', on="id")
    #print(finalgrid)
    insc_nodes = np.array(finalgrid["infra_score"])
    insc_ways  = np.array(dfgridnew["infra_score"])
    print("Fun facts:")
    print("Nodes:")
    print("\tµ = ", np.mean(np.array(insc_nodes)))
    print("\tσ = ", np.std (np.array(insc_nodes)))
    print("Ways:")
    print("\tµ = ", np.mean(np.array(insc_ways)))
    print("\tσ = ", np.std (np.array(insc_ways)))

    #normalisieren
    insc = -insc_nodes - insc_ways
    insc = insc/np.max(np.abs(insc)) + 1
    finalgrid["infra_score"] =  insc

    #print("Gebäudeumrisse mit Infrastrukturwert: ")
    #print(poly)

    print("Generated grid:")
    print(finalgrid)
    finalgrid.to_file(driver="ESRI Shapefile", filename=sys.argv[3])
    print("Saved grid to file: " + sys.argv[3])
    print("Finished")
    print("--- "+ str(round((time.time() - start_time), 2)) + " seconds ---")
    return

main()
