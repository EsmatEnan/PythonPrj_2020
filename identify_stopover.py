import os
from qgis.core import *
import qgis.utils
import ogr
import pandas as pd

#user input
in_file = r"E:\Munster\python\final project\movebank\goose\outputs\points_reprojected.shp"
out_fn = r"E:\Munster\python\final project\movebank\goose\outputs\stopovers.shp"
new_layer_name = 'stopovers'

ds=driver.Open(in_file,1)

# Check to see if shapefile is found.
if ds is None:
    print('Could not open %s' % (in_file))

in_lyr = ds.GetLayer(0)

# Delete if output file already exists
if os.path.exists(out_fn):
    print('exists, deleting')
    driver.DeleteDataSource(out_fn)
    
out_ds = driver.CreateDataSource(out_fn)
if out_ds is None:
    print('Could not open %s' % (out_fn))

#crate the output layer
out_lyr = out_ds.CreateLayer(new_layer_name,
                             in_lyr.GetSpatialRef(),
                             ogr.wkbPoint)


out_defn = out_lyr.GetLayerDefn()
out_feat = ogr.Feature(out_defn)

# Get the id of the each bird
birds = ['79698', '73053', '72417', '72364', '72413', '79694', '73054']


for bird in birds:
    lats=[]
    lngs=[]
    times=[]
    total_distance = 0
    
    #filter the layer depend on the bird id
    in_lyr.SetAttributeFilter("ind_ident = " "'"+bird+"'")
    
    #iterate throught the filtered features 
    for feat in in_lyr:
        dis = feat.GetField('dist_prv')
        time = feat.GetField('timestamp')
        lat = feat.GetField('lat')
        long = feat.GetField('long')
        lats.append(lat)
        lngs.append(long)
        times.append(time)
        if dis is not None:
            total_distance += dis
            
        # Check if the disatnce more than 30km
        if total_distance > 30000:
            
            # put the timestamp into a series and convert it to data time
            x = pd.Series(times)
            x = pd.to_datetime(x)
            x_list = x.tolist()
            #CHECK the time difference between the first anl last point
            # "the distance < 5000" condition to make sure, there is no a big gap betwwen the gps points in the last distance
            time_diff = (x_list[-1] - x_list[0]).days
            if (time_diff >= 2 and dis < 5000):
                #caclulate the center of the group
                avg_lat = sum(lats) / len(lats)
                avg_lng = sum(lngs) / len(lngs)
                # create the WKT for the feature 
                wkt = "POINT(%f %f)" %  (float(avg_lng) , float(avg_lat))
                # Create the point from the Well Known Txt
                point = ogr.CreateGeometryFromWkt(wkt)
                # create the stopover point inside the output layer
                out_feat.SetGeometry(point)
                out_lyr.CreateFeature(out_feat)
                #reset the variables to group other points
                lats=[]
                lngs=[]
                times=[]
                total_distance = 0
            else:
                #reset the variables to group other points
                lats=[]
                lngs=[]
                times=[]
                total_distance = 0
            

    
del out_ds
print('done')    
