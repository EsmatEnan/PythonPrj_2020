from matplotlib import pyplot as plt
import gdal,copy
import numpy as np
import ogr
import os

#############

dir_vector = r"E:\Munster\python\final project\movebank\goose\outputs\stopovers3.shp"
dir_raster = r"E:\Munster\python\final project\movebank\goose\outputs\clipped_raster.tif"



# Getting the correct driver and open vector file for reading
driver = ogr.GetDriverByName('ESRI Shapefile')
track = driver.Open(dir_vector, 0)
# Getting the layer
layer = track.GetLayer(0)


# Getting Raster value as numpy array
rastData = gdal.Open(dir_raster, 1)
in_band = rastData.GetRasterBand(1)

array = np.array(in_band.ReadAsArray())
values = np.unique(array)
value = values.tolist()

colors = gdal.ColorTable()
for i in value:
    print (i)
    colors.SetColorEntry(i, (0,0,255))
 
in_band.SetRasterColorTable(colors)
rastData.FlushCache()

data = in_band.ReadAsArray()

# Create the plot
f, axarr = plt.subplots(1)

#  imshow to plot the raster
im = axarr.imshow(data)

plt.show()

del rastData, in_band







