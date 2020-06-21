
import gdal
import ogr
import osr
import os

#Locating the raster
raster_data = "C:/Users/enan/Desktop/PIG_Prj/Landuse/gm_lc_v3_1_2.tif"
#Locating the vector
vecPoint = "C:/Users/enan/Desktop/PIG_Prj/Prj/pointsPrj.shp"

# accessing the land use data
rast_data_source = gdal.Open(raster_data)
# Getting reference system info form land use
rast_spatial_ref = rast_data_source.GetSpatialRef()
print(' Spatial reference of the raster data is', rast_spatial_ref)

# Get the correct driver
driver = ogr.GetDriverByName('ESRI Shapefile')

# 0 means read-only. 1 means writeable.
vect_data_source = driver.Open(vecPoint, 0) 

# Checking to see if shapefile is found.
if vect_data_source is None:
    print("Sorry! File couldn`t find" )
print("-----------------------------------------------------------------------")

# Getting the Layer class object
layer = vect_data_source.GetLayer(0)
# Getting reference system info form points
vect_spatial_ref = layer.GetSpatialRef()
print('Spatial reference of the vector data is', vect_spatial_ref)

#Comparing the both ref system info
if vect_spatial_ref == rast_spatial_ref :
  print("Ypu don`t  need to transfer projections system")
else:
  print("You need to transfer projections system ")