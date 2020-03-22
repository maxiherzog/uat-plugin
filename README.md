# unnecessary-activity-tracker

A tool to identify and visualize necessary and unnecessary movement of people using positional data(e.g. anonymized cell phone data)

This project was made in 48h hours _from 20.3 to 22.3.20_ during the [#WirVsWirus](http://www.wirvsvirushackathon.org) -Hackathon, to contribute in finding solutions to the on-going corona-crisis.
Also see the corresponding [devpost-page](https://devpost.com/software/0045_haustiere_handydaten)(in German).
Feel free to pull request and help continuing the development of this tool!

### Dependencies
You'll need Python3.x and the following modules:
_overpy, numpy, pandas, geopandas, rtree_
You can install them using pip or anaconda!

## Generating the Infrastrucure
A Shape File of the grid(the .shp and .shx files), and a Table with tagweights.
If you got those you can run
```
python3 grid_infra_score_gen.py GRID.shp TAG_WEIGHTS.csv INFRA_SCORES.shp
```
Keep in mind that this generates 4 filetypes: cpg, dbf, prj, shp, shx
If you set this Tool up on a server, you might consider running this very rarely, because the infra_score won't change much over time.

## Generating the Shape File
If you got your files(especially the .shp and .shx) you can run
```
python3 main.py GRID.shp INFRA_SCORES.shp POINTS.shp POINTS_BACKGROUND.shp SCORES_FINAL.shp
```
Where POINTS.shp is the Shape File for the Location-Data, and POINTS_BACKGROUND.shp is the background noise of given Point distribution.(e.g. at night)
This generates 4 filtypes for the Shape file with values 
* **geometry** The Grids geometries to display in any compatible program 
* **val** The calculated value of unnecessary-movement calculated with a(pop, infra)= pop^infra + pop
* **pop** The caculated value of movement
* **infra** The generated values for the surrounding infra structure

## Built With

* [Overpass](https://github.com/drolbr/Overpass-API) - The API used to access OSM
* [overpy](https://github.com/DinoTools/python-overpy) - Python Wrapper to access the Overpass-API
* [geopandas](https://geopandas.org/) - Mapping Python Library build on pandas to create and import Shape Files
* [QGis](https://www.qgis.org/de/site/index.html) - Used to display Shape Files
