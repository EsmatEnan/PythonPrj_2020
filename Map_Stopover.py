####Import Dependencies####

from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches
import gdal,copy
import numpy as np
import ogr
import os

#  File Directory
dir_vector = "C:/Users/enan/Desktop/PIG_Prj/Stopover/stopovers.shp"
dir_raster = "C:/Users/enan/Desktop/PIG_Prj/Landuse/clipped_raster_byte.tif"

# Creating the plot
f, axarr = plt.subplots(1)
# Accessing the raster and read out the data in a numpy array
rastData = gdal.Open(dir_raster)
in_band = rastData.GetRasterBand(1)
data = in_band.ReadAsArray()

#GetGeoTransform and specify the extent
geoTransform = rastData.GetGeoTransform()
minx = geoTransform[0]
maxy = geoTransform[3]
maxx = minx + geoTransform[1] * \
      rastData.RasterXSize
miny = maxy + geoTransform[5] * \
       rastData.RasterYSize
ext=(minx, maxx, miny, maxy)

#Reclass Raster Value
rast_array = data.astype(np.float)
rastAr_reclass = copy.copy(rast_array)
rastAr_reclass[np.where(rast_array==0)] = 1 
rastAr_reclass[np.where(rast_array==1)] = 2
rastAr_reclass[np.where(rast_array==2)] = 3
rastAr_reclass[np.where(rast_array==3)] = 4
rastAr_reclass[np.where(rast_array==4)] = 5
rastAr_reclass[np.where(rast_array==5)] = 6
rastAr_reclass[np.where(rast_array==6)] = 7
rastAr_reclass[np.where(rast_array==7)] = 8
rastAr_reclass[np.where(rast_array==8)] = 9
rastAr_reclass[np.where(rast_array==9)] = 10
rastAr_reclass[np.where(rast_array==10)] = 11
rastAr_reclass[np.where(rast_array==11)] = 12
rastAr_reclass[np.where(rast_array==12)] = 13
rastAr_reclass[np.where(rast_array==13)] = 14
rastAr_reclass[np.where(rast_array==14)] = 15
rastAr_reclass[np.where(rast_array==15)] = 16
rastAr_reclass[np.where(rast_array==16)] = 17
rastAr_reclass[np.where(rast_array==17)] = 18
rastAr_reclass[np.where(rast_array==18)] = 19
rastAr_reclass[np.where(rast_array==19)] = 20

#Specifying color limit
classColo = colors.ListedColormap(['lime','yellow','orange','green','red','gray','gold','darkgoldenrod','brown','forestgreen','violet',
'sienna','lightgreen','olive','teal','cyan','slategray','rosybrown','sandybrown','blue'])
# imshow to plot the raster
plt.imshow(rastAr_reclass,extent=ext,cmap=classColo)

#Create custom legend to label the Land Cover Classes and Goose Stop Points
stopP = mpatches.Patch(color='black', label='Stop Points')
lCC_1  = mpatches.Patch(color='lime', label='Broadleaf Evergreen Forest')
lCC_2  = mpatches.Patch(color='yellow', label='Broadleaf Deciduous Forest')
lCC_3  = mpatches.Patch(color='orange', label='Needleleaf Evergreen Forest')
lCC_4  = mpatches.Patch(color='green', label='Needleleaf Deciduous Forest')
lCC_5  = mpatches.Patch(color='red', label='Mixed Forest')
lCC_6  = mpatches.Patch(color='gray', label='Tree Open')
lCC_7 = mpatches.Patch(color='gold', label='Shrub')
lCC_8 = mpatches.Patch(color='darkgoldenrod', label='Herbaceous')
lCC_9  = mpatches.Patch(color='brown', label='Tree/Shrub')
lCC_10  = mpatches.Patch(color='forestgreen', label='Sparse vegetation')
lCC_11 = mpatches.Patch(color='violet', label='Cropland')
lCC_12 = mpatches.Patch(color='sienna', label='Paddy field')
lCC_13 = mpatches.Patch(color='lightgreen', label='Cropland/Other Vegetation Mosaic')
lCC_14 = mpatches.Patch(color='olive', label='Mangrove')
lCC_15 = mpatches.Patch(color='teal', label='Wetland')
lCC_16 = mpatches.Patch(color='cyan', label='gravel,rock')
lCC_17 = mpatches.Patch(color='slategray', label='sand')
lCC_18 = mpatches.Patch(color='rosybrown', label='Urban')
lCC_19 = mpatches.Patch(color='sandybrown', label='Snow/Ic')
lCC_20 = mpatches.Patch(color='blue', label='Water bodies')

#Combining all the classes with stop points in a single frame
lCC_point=[stopP,lCC_1,lCC_2,lCC_3,lCC_4,lCC_5,lCC_6,lCC_7,lCC_8,lCC_9,lCC_10,lCC_11,lCC_12,lCC_13,lCC_14,lCC_15,lCC_16,lCC_17,lCC_18,lCC_19,lCC_20]

# Getting the correct driver and open vector file for reading
driver = ogr.GetDriverByName('ESRI Shapefile')
gPoint = driver.Open(dir_vector, 0)

# Getting the layer
layer = gPoint.GetLayer(0)

# Accessing every feature to plot
x = []
y = []
for feat in layer:
    pt = feat.geometry()
    x.append(pt.GetX())
    y.append(pt.GetY())
   
# Making the scatter plot
scat = axarr.plot(x, y,'ko')
axarr.set_xlabel('Longitude')
axarr.set_ylabel('Latitude')
axarr.tick_params(axis='both', labelsize=8)
axarr.set_aspect('equal')
plt.title('Land cover with Goose stop points')
axarr.legend(handles=lCC_point,loc='lower center', bbox_to_anchor=(0.5,-0.5),
          fancybox=True, ncol=5)
plt.show()

##Finish##


