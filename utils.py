#!/usr/bin/env python
# coding: utf-8

# In[195]:

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox
import pandas as pd
import pickle

# In[2]:

path = r"Y:\RECHERCHE ET DEV\10_Modèle d'attractivite des rues\04_données clients (source)\osm\paris"

# In[136]:

# In[139]:


#get iris of a building
def get_iris(building_ID, contour_iris, iris_data, buildings, display=True):

    mask = contour_iris.intersects(
        buildings.loc[building_ID]['geometry']).to_numpy()
    if display:
        fig, ax = plt.subplots()
        contour_iris[mask].plot(ax=ax)
        buildings.loc[[building_ID]].plot(ax=ax, color="red")
        plt.show()

    return iris_data.loc[contour_iris[mask]['CODE_IRIS'].values]


# In[1]:


#get all buildings in a iris_id
def get_buildings_iris(iris_id,
                       contour_iris=None,
                       iris_data=None,
                       buildings=None,
                       display=True):

    if contour_iris is None:
        contour_iris = gpd.read_file(
            r'Y:\REFERENTIEL DATA\RP 2022 FRANCE\CARTOGRAPHIE\Cartographie_France_IRIS_2019\CONTOURS-IRIS_2-1_SHP_LAMB93_FXX-2019\CONTOURS-IRIS.shp'
        ).to_crs('EPSG:3857')
    if iris_data is None:
        iris_data = pd.read_excel(
            'Y:\REFERENTIEL DATA\RP 2022 FRANCE\GEODATA - IRIS\Geodata_IRIS_essentiels.xlsx'
        )
    if buildings is None:
        buildings = pickle.load(
            open(path + r'\building_level_filled.pkl',
                 'rb')).to_crs('EPSG:3857')

    mask = buildings.intersects(contour_iris[
        contour_iris["CODE_IRIS"] == iris_id].iloc[0]['geometry']).to_numpy()

    if display and mask.any():
        fig, ax = plt.subplots()
        contour_iris[contour_iris["CODE_IRIS"] == iris_id].plot(ax=ax)
        buildings[mask].plot(ax=ax, color="#71DAFF")
        plt.show()
    return buildings[mask]
