from shapely.geometry import MultiLineString
from shapely.ops import polygonize
import geopandas as gpd 
import numpy as np


bottomLeft = (-10,49)
bottomRight = (2,49)
topLeft = (-10,59)
topRight = (2,59)

gadm_1 = gpd.read_file(r"/home/joyce/Projects/Flood_Tweet_Project/data/Shapefiles/UK/GBR_adm/GBR_adm1.shp")
gadm_1 = gadm_1.to_crs(4326)
gadm_england = gpd.GeoSeries(gadm_1.iloc[0].geometry)

cols = np.linspace(bottomLeft[1], topLeft[1], num=100)
rows = np.linspace(bottomLeft[0], bottomRight[0], num=100)

x = rows
y = cols

hlines = [((x1, yi), (x2, yi)) for x1, x2 in zip(x[:-1], x[1:]) for yi in y]
vlines = [((xi, y1), (xi, y2)) for y1, y2 in zip(y[:-1], y[1:]) for xi in x]

grids = list(polygonize(MultiLineString(hlines + vlines)))
grids = gpd.GeoSeries(grids)

in_map = np.array([grids.within(geom) for geom in gadm_england])
in_map = in_map.sum(axis=0)

pls= gpd.GeoSeries([val for pos,val in enumerate(grids) if in_map[pos]])
england_grid = gpd.GeoDataFrame(pls,geometry = pls)
england_grid.crs = "EPSG:4326"

grid = england_grid["geometry"]
grid.to_file("../data/grids/england{0}x{1}.shp".format(len(cols),len(rows)))