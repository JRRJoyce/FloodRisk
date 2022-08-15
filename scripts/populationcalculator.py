import geopandas as gpd
from shapely.strtree import STRtree
import pandas as pd
import numpy as np
from tqdm import tqdm
import csv

england_grid =gpd.read_file("../notebooks/england200x200.shp")
lsoa2011 = gpd.read_file(r"/home/joyce/Projects/Flood_Tweet_Project/data/Shapefiles/SOAs/Lower_Layer_Super_Output_Areas_December_2011_Generalised_Clipped__Boundaries_in_England_and_Wales/Lower_Layer_Super_Output_Areas_December_2011_Generalised_Clipped__Boundaries_in_England_and_Wales.shp")
lsao2011 = lsoa2011.to_crs(4326)
lsoa_census = pd.read_csv(r"../data/Population_data/R1_4_EW__RT__Table_PHP01___LSOA_MSOA_v4.csv")
combined = pd.merge(lsoa2011,lsoa_census, left_on = ["lsoa11nm"], right_on = ["LSOA Name"] )
combined["Persons:All usual residents"] = combined["Persons:All usual residents"].str.replace(',', '').astype(int)

s = STRtree(combined["geometry"])
querygeom = england_grid["geometry"]

population = []
for geo in tqdm(querygeom):
    pop = 0
    result=s.query(geo)
    for poly in result:
        index = np.where(combined["geometry"] == poly)
        #index = combined[combined[\"geometry\"]==poly].index.values
        index_pop = combined["Persons:All usual residents"].iloc[index].values[0]
        pop += (poly.intersection(geo).area/poly.area)*index_pop
    population.append(pop)

with open("../data/Population_data/200x200grid.csv", 'w', newline='') as myfile:
     wr = csv.writer(myfile)
     wr.writerow(population)
