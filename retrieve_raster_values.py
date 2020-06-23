# This code is from: https://gis.stackexchange.com/questions/76909/load-raster-values-into-shapefile
# But gives the following error:
#          TypeError: a bytes-like object is required, not 'NoneType'
# From what I have searched, it's because this code was developed in
# a old python version, trying to figure it out. But it's the only option of doing
# this task using QGIS/Open Source Library

from osgeo import gdal,ogr
import struct

work_dir = os.path.join('C:\\', 'Users', 'pablo', 'Documents', 'ifgi_Munster', 
                            'pythonGIS_DEM', 'project_data')
src_filename = os.path.join(work_dir, 'gm_lc_v3_1_2.tif')
shp_filename = os.path.join(work_dir, 'reproj', 'route_point_reproj.shp')

src_ds=gdal.Open(src_filename) 
gt=src_ds.GetGeoTransform()
rb=src_ds.GetRasterBand(1)

ds=ogr.Open(shp_filename,1)
lyr=ds.GetLayer()
# Add a new field
new_field = ogr.FieldDefn('VALUE', ogr.OFTInteger)
lyr.CreateField(new_field)

for feat in lyr:
    geom = feat.GetGeometryRef()
    mx,my=geom.GetX(), geom.GetY()  #coord in map units

    #Convert from map to pixel coordinates.
    #Only works for geotransforms with no rotation.
    #If raster is rotated, see http://code.google.com/p/metageta/source/browse/trunk/metageta/geometry.py#493
    px = int((mx - gt[0]) / gt[1]) #x pixel
    py = int((my - gt[3]) / gt[5]) #y pixel

    structval=rb.ReadRaster(px,py,1,1,buf_type=gdal.GDT_UInt32) #Assumes 16 bit int aka 'short'
    intval = struct.unpack('h' , structval) #use the 'short' format code (2 bytes) not int (4 bytes)

    #print intval[0] #intval is a tuple, length=1 as we only asked for 1 pixel value
    feat.SetField('VALUE', intval[0]) 
    # trigger the update
    lyr.SetFeature(feat)

# Close the Shapefile
ds = None