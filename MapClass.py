from matplotlib import pyplot as plt
import gdal,copy
import numpy as np
import ogr
import os

#############

dir_vector = "C:/Users/enan/Desktop/PIG_Prj/Stopover/stopovers.shp"
dir_raster = "C:/Users/enan/Desktop/PIG_Prj/Landuse/clipped_raster_byte.tif"

# Create the plot
f, axarr = plt.subplots(1)

# Getting Raster value as numpy array
rastData = gdal.Open(dir_raster)
in_band = rastData.GetRasterBand(1)
data = in_band.ReadAsArray()

geoTransform = rastData.GetGeoTransform()
minx = geoTransform[0]
maxy = geoTransform[3]
maxx = minx + geoTransform[1] * \
      rastData.RasterXSize
miny = maxy + geoTransform[5] * \
       rastData.RasterYSize

#  imshow to plot the raster
im = axarr.imshow(data, extent=(minx, maxx, miny, maxy))
cb = plt.colorbar(im, orientation='horizontal',spacing='unique')
cb.set_label('Land cover value')

# Getting the correct driver and open vector file for reading
driver = ogr.GetDriverByName('ESRI Shapefile')
track = driver.Open(dir_vector, 0)

# Getting the layer
layer = track.GetLayer(0)

# Accessing very feature to plot
x = []
y = []
for feat in layer:
    pt = feat.geometry()
    x.append(pt.GetX())
    y.append(pt.GetY())
   
# Making the scatter plot
scat = axarr.plot(x, y,'bo')
cb = plt.legend(scat,['Stop Points'])
axarr.set_xlabel('Longitude')
axarr.set_ylabel('Latitude')
axarr.tick_params(axis='both', labelsize=8)
axarr.set_aspect('equal')
plt.title('Land cover raster and Goose stop points')
plt.show()