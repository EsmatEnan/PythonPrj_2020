import numpy as np
import gdal, copy
import matplotlib.pyplot as plt
import warnings

dir_vector = "C:/Users/enan/Desktop/PIG_Prj/Stopover/stopovers.shp"
chm_filename = "C:/Users/enan/Desktop/PIG_Prj/Landuse/clipped_raster_byte.tif"

chm_dataset = gdal.Open(chm_filename)
cols = chm_dataset.RasterXSize;
rows = chm_dataset.RasterYSize;

chm_mapinfo = chm_dataset.GetGeoTransform()
xMin = chm_mapinfo[0]
yMax = chm_mapinfo[3]

xMax = xMin + chm_dataset.RasterXSize/chm_mapinfo[1] #divide by pixel width 
yMin = yMax + chm_dataset.RasterYSize/chm_mapinfo[5] #divide by pixel height (note sign +/-)
chm_ext = (xMin,xMax,yMin,yMax)

chm_raster = chm_dataset.GetRasterBand(1)
scaleFactor = chm_raster.GetScale()


chm_array = chm_dataset.GetRasterBand(1).ReadAsArray(0,0,cols,rows).astype(np.float)
chm_array=chm_array/scaleFactor

def plot_spatial_array(band_array,spatial_extent,colorlimit,ax=plt.gca(),title='',cmap_title='',colormap=''):
    plot = plt.imshow(band_array,extent=spatial_extent,clim=colorlimit); 
    cbar = plt.colorbar(plot,aspect=40); plt.set_cmap(colormap); 
    cbar.set_label(cmap_title,rotation=90,labelpad=20);
    plt.title(title); ax = plt.gca(); 
    ax.ticklabel_format(useOffset=False, style='plain'); #do not use scientific notation #
    rotatexlabels = plt.setp(ax.get_xticklabels(),rotation=90); #rotate x tick labels 90 degrees
    

chm_reclass = copy.copy(chm_array)
chm_reclass[np.where(chm_array==0)] = 1 
chm_reclass[np.where(chm_array==1)] = 2
chm_reclass[np.where(chm_array==2)] = 3
chm_reclass[np.where(chm_array==3)] = 4
chm_reclass[np.where(chm_array==4)] = 5
chm_reclass[np.where(chm_array==5)] = 6
chm_reclass[np.where(chm_array==6)] = 7
chm_reclass[np.where(chm_array==7)] = 8
chm_reclass[np.where(chm_array==8)] = 9
chm_reclass[np.where(chm_array==9)] = 10
chm_reclass[np.where(chm_array==10)] = 11
chm_reclass[np.where(chm_array==11)] = 12
chm_reclass[np.where(chm_array==12)] = 13
chm_reclass[np.where(chm_array==13)] = 14
chm_reclass[np.where(chm_array==14)] = 15
chm_reclass[np.where(chm_array==15)] = 16
chm_reclass[np.where(chm_array==16)] = 17
chm_reclass[np.where(chm_array==17)] = 18
chm_reclass[np.where(chm_array==18)] = 19
chm_reclass[np.where(chm_array==19)] = 20



import matplotlib.colors as colors
plt.figure(); 
cmapCHM = colors.ListedColormap(['lightblue','yellow','orange','green','red','black','gold','darkred','forestgreen','violet',
'sienna','lightgreen','olive','teal','crimson','slategray','rosybrown','sandybrown','blue'])
plt.imshow(chm_reclass,extent=chm_ext,cmap=cmapCHM)
plt.title('Land Cover class')
ax=plt.gca(); ax.ticklabel_format(useOffset=False, style='plain') #do not use scientific notation 

# Create custom legend to label the four canopy height classes:
import matplotlib.patches as mpatches
class1_box = mpatches.Patch(color='lightblue', label='Broadleaf Evergreen Forest')
class2_box = mpatches.Patch(color='yellow', label='Broadleaf Deciduous Forest')
class3_box = mpatches.Patch(color='orange', label='Needleleaf Evergreen Forest')
class4_box = mpatches.Patch(color='green', label='Needleleaf Deciduous Forest')
class5_box = mpatches.Patch(color='red', label='TMixed Forest')
class6_box = mpatches.Patch(color='black', label='Tree Open')
class7_box = mpatches.Patch(color='gold', label='Shrub')
class8_box = mpatches.Patch(color='darkred', label='Herbaceous')
class9_box = mpatches.Patch(color='red', label='Tree/Shrub')
class10_box = mpatches.Patch(color='forestgreen', label='Sparse vegetation')
class11_box = mpatches.Patch(color='violet', label='Cropland')
class12_box = mpatches.Patch(color='sienna', label='Paddy field')
class13_box = mpatches.Patch(color='lightgreen', label='Cropland/Other Vegetation Mosaic')
class14_box = mpatches.Patch(color='olive', label='Mangrove')
class15_box = mpatches.Patch(color='teal', label='Wetland')
class16_box = mpatches.Patch(color='crimson', label='gravel,rock')
class17_box = mpatches.Patch(color='slategray', label='sand')
class18_box = mpatches.Patch(color='rosybrown', label='Urban')
class19_box = mpatches.Patch(color='sandybrown', label='Snow/Ic')
class20_box = mpatches.Patch(color='blue', label='Water bodies')
classbox=[class1_box,class2_box,class3_box,class4_box,class5_box,class6_box,class7_box,class8_box,class9_box,class10_box,
class11_box,class12_box,class13_box,class14_box,class15_box,class16_box,class17_box,class18_box,class19_box,class20_box]

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

ax.legend(handles=classbox,
          loc='best',borderaxespad=0.)

