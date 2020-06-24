import os
import gdal
import ogr


<<<<<<< HEAD
raster = r"E:\Munster\python\final project\Data\gm_lc_v3_1_2.tif"
rast_data_source = gdal.Open(raster)

####### Cropping the raster #######

reproj_shp = r"E:\Munster\python\final project\movebank\goose\outputs\pointsPrj.shp"
=======
raster = os.path.join(work_dir, 'gm_lc_v3_1_2.tif')
raster_ds = gdal.Open(raster)

####### Cropping the raster #######

reproj_shp = os.path.join(work_dir, 'reproj', 'points_rpj.shp')
>>>>>>> 5c93bf3faebc5df1d0c35122700b042c14e1c5f8
driver = ogr.GetDriverByName('ESRI Shapefile')
shape = driver.Open(reproj_shp, 0)
shp_lyr = shape.GetLayer(0)

#Extent of Shapefile
x_min, x_max, y_min, y_max = shp_lyr.GetExtent()
print("Shapefile bounding box coordinates:", x_min, x_max, y_min, y_max)


# Getting the object to translate coordinates to indices
gt = raster_ds.GetGeoTransform()
inv_gt = gdal.InvGeoTransform(gt)

# Converting BBox coordinates to raster indices
buffer = 1000

x1, y1= gdal.ApplyGeoTransform(inv_gt, x_min - buffer, y_min - buffer)
x2, y2= gdal.ApplyGeoTransform(inv_gt, x_max + buffer, y_max + buffer)

# Turning indices into integers variables
x1 = int(round(x1))
y1 = int(round(y1))
x2 = int(round(x2))
y2 = int(round(y2))
print("Lower left corner indice:", x1, y1, '\t', "Upper Right Corner indice:", x2, y2)

#Clipping Settings
out_columns = x2 - x1
out_rows = y1 - y2
print("output raster extent is:", out_columns, out_rows)

#Output Clipped Raster
<<<<<<< HEAD
clipped_raster = r"E:\Munster\python\final project\movebank\goose\outputs\clipped_raster.tif"
=======
clipped_raster = os.path.join(work_dir,'clipped_gm_lc.tif')
>>>>>>> 5c93bf3faebc5df1d0c35122700b042c14e1c5f8
driver = gdal.GetDriverByName("GTiff")
out_ds = driver.Create(clipped_raster, out_columns, out_rows, 1, gdal.GDT_UInt32)
out_ds.SetProjection(raster_ds.GetProjection())

# Applying Geotransform
out_gt = list(gt)
out_gt[0] = x_min - 2*buffer
out_gt[3] = y_max + 2*buffer
print(out_gt)
out_ds.SetGeoTransform(out_gt)

# Writing new raster from the input raster
in_raster = raster_ds.GetRasterBand(1)
out_raster = out_ds.GetRasterBand(1)
data = in_raster.ReadAsArray(x1, y2, out_columns, out_rows)
out_raster.WriteArray(data)
out_ds.FlushCache()
print('done')