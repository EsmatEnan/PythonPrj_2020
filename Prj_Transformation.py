import gdal
import ogr
import os
import osr
# Locating the land use data
raster = "C:/Users/enan/Desktop/PIG_Prj/Landuse/gm_lc_v3_1_2.tif"
# Locating the goose point data
vecPoint = "C:/Users/enan/Desktop/PIG_Prj/Goose/points.shp"

# Locating ouput file ptah
out_file = "C:/Users/enan/Desktop/PIG_Prj/Prj/pointsPrj.shp"

# Access the land use
rast_data_source = gdal.Open(raster)
# Getting spatial reference info of the lad use data
rast_spatial_ref = rast_data_source.GetProjection()
print('Spatial reference system of the raster is: ', rast_spatial_ref)

# Getting the correct driver
driver = ogr.GetDriverByName('ESRI Shapefile')

#Access the goose pint file
vect_data_source = driver.Open(vecPoint, 0) 

# Checking file existence.
if vect_data_source is None:
    print("Sorry the file doesn`t exist")

# Get the Layer class object
layer = vect_data_source.GetLayer(0)
# Getting spatial reference info of the goose point data
vect_spatial_ref = layer.GetSpatialRef()
print('Spatial reference system of the vector is: ', vect_spatial_ref)

# creating osr object of land use`s spatial ref info
sr = osr.SpatialReference(rast_spatial_ref)
transform = osr.CoordinateTransformation(vect_spatial_ref, sr)

# Deleting if output file already exists

if os.path.exists(out_file):
    print('Please wait to remoeve the existing file')
    driver.DeleteDataSource(out_file)
out_ds = driver.CreateDataSource(out_file)
if out_ds is None:
    print("Wait please")

# Creating a new shapefile layer using SR
out_lyr = out_ds.CreateLayer('pointsPrj', sr, 
                             ogr.wkbPoint)

out_lyr.CreateFields(layer.schema)
out_defn = out_lyr.GetLayerDefn()
out_feat = ogr.Feature(out_defn)
# Loop over all features and changing the spatial ref
for in_feat in layer:
    geom = in_feat.GetGeometryRef()
    geom.Transform(transform)
    out_feat.SetGeometry(geom)
    # Adding the attributes in the new file
    for i in range(out_defn.GetFieldCount()):
        value = in_feat.GetField(i)
        out_feat.SetField(out_defn.GetFieldDefn(i).GetNameRef(), value)
    out_lyr.CreateFeature(out_feat)

del out_ds

print('Projection Tansformation has been done')





