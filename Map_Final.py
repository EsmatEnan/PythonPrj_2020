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

#Create custom legend to label the Land Cover Classes and Goose Stop Points
class1_box = mpatches.Patch(color='black', label='Stop Points')
class2_box = mpatches.Patch(color='lime', label='Broadleaf Evergreen Forest')
class3_box = mpatches.Patch(color='yellow', label='Broadleaf Deciduous Forest')
class4_box = mpatches.Patch(color='orange', label='Needleleaf Evergreen Forest')
class5_box = mpatches.Patch(color='green', label='Needleleaf Deciduous Forest')
class6_box = mpatches.Patch(color='red', label='Mixed Forest')
class7_box = mpatches.Patch(color='gray', label='Tree Open')
class8_box = mpatches.Patch(color='gold', label='Shrub')
class9_box = mpatches.Patch(color='darkgoldenrod', label='Herbaceous')
class10_box = mpatches.Patch(color='brown', label='Tree/Shrub')
class11_box = mpatches.Patch(color='forestgreen', label='Sparse vegetation')
class12_box = mpatches.Patch(color='violet', label='Cropland')
class13_box = mpatches.Patch(color='sienna', label='Paddy field')
class14_box = mpatches.Patch(color='lightgreen', label='Cropland/Other Vegetation Mosaic')
class15_box = mpatches.Patch(color='olive', label='Mangrove')
class16_box = mpatches.Patch(color='teal', label='Wetland')
class17_box = mpatches.Patch(color='cyan', label='gravel,rock')
class18_box = mpatches.Patch(color='slategray', label='sand')
class19_box = mpatches.Patch(color='rosybrown', label='Urban')
class20_box = mpatches.Patch(color='sandybrown', label='Snow/Ic')
class21_box = mpatches.Patch(color='blue', label='Water bodies')
classbox=[class1_box,class2_box,class3_box,class4_box,class5_box,class6_box,class7_box,class8_box,class9_box,class10_box,
class11_box,class12_box,class13_box,class14_box,class15_box,class16_box,class17_box,class18_box,class19_box,class20_box,class21_box]

#Specifying color
cmapCHM = colors.ListedColormap(['lime','yellow','orange','green','red','gray','gold','darkgoldenrod','brown','forestgreen','violet',
'sienna','lightgreen','olive','teal','cyan','slategray','rosybrown','sandybrown','blue'])
# imshow to plot the raster
plt.imshow(rastAr_reclass,extent=ext,cmap=cmapCHM)

# Getting the correct driver and open vector file for reading
driver = ogr.GetDriverByName('ESRI Shapefile')
track = driver.Open(dir_vector, 0)

# Getting the layer
layer = track.GetLayer(0)

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
plt.title('Land cover and Goose stop points')
axarr.legend(handles=classbox,loc='lower center', bbox_to_anchor=(0.5,-0.5),
          fancybox=True, ncol=5)
plt.show()

##END##


