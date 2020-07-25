import os
import gdal
import ogr

data_dir = r"E:\Munster\python\final project\Data"
raster = os.path.join(data_dir,'gm_lc_v3_1_2.tif')
reproj_shp = os.path.join(data_dir, 'goose', 'points.shp')
buffer = 2 # unit: degrees

clipped_raster = os.path.join(data_dir, 'clipped_raster_byte3.tif')

rast_data_source = gdal.Open(raster)

####### Cropping the raster #######

driver = ogr.GetDriverByName('ESRI Shapefile')
shape = driver.Open(reproj_shp, 0)
shp_lyr = shape.GetLayer(0)

#BoundingBox of Shapefile
x_min, x_max, y_min, y_max = shp_lyr.GetExtent()
print("GetExtent returned", x_min, x_max, y_min, y_max)


# Getting the object to translate coordinates to indices
gt = rast_data_source.GetGeoTransform()
inv_gt = gdal.InvGeoTransform(gt)
# Converting BBox coordinates to raster indices
x1, y1= gdal.ApplyGeoTransform(inv_gt, x_min - buffer, y_min - buffer)
x2, y2= gdal.ApplyGeoTransform(inv_gt, x_max + buffer, y_max + buffer)

# Turning indices into integers variables
x1 = int(x1)
y1 = int(y1)
x2 = int(x2)
y2 = int(y2)
print("Lower left corner:", x1, y1, '\t', "Upper Right Corner:", x2, y2)



#Clipping Settings
out_columns = x2 - x1 
out_rows = y1 - y2 

#Output Clipped Raster
driver = gdal.GetDriverByName("GTiff")
print("Out size", out_columns, out_rows)
out_ds = driver.Create(clipped_raster, out_columns, out_rows, 1, gdal.GDT_Byte)
projection = rast_data_source.GetProjection()
out_ds.SetProjection(projection)

# Applying Geotransform
out_gt = list(gt)
out_gt[0] = x_min - buffer
out_gt[3] = y_max  + buffer
print(out_gt)
out_ds.SetGeoTransform(out_gt)

# Writing new raster from the input raster
in_raster = rast_data_source.GetRasterBand(1)
out_raster = out_ds.GetRasterBand(1)
data = in_raster.ReadAsArray(x1, y2, out_columns, out_rows)
out_raster.WriteArray(data)
out_ds.FlushCache()
print('done')
