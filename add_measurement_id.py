import os
from qgis.core import *
import qgis.utils

# path to shapefile we want to add the new field
data_dir = r"C:\Users\efthy\Documents\MasterGeoTech\semester2\Python\Project\data"
shape_file = os.path.join(data_dir, 'goose', 'points_reprojected.shp')

layer = iface.addVectorLayer(shape_file, "shape:", "ogr")

if not layer:
    print("Shapefile failed to load!")

## Check for editing rights (capabilities)
caps = layer.dataProvider().capabilities()

## Adding a field (attribute)
if caps & QgsVectorDataProvider.AddAttributes:
    res = layer.dataProvider().addAttributes([QgsField("point_id", QVariant.String)])
print(res)
layer.updateFields()

fields = layer.fields()
field_idx = fields.indexFromName('point_id')
print(field_idx)

i = 0
for feat in layer.getFeatures():
    i += 1
    attr = { field_idx : str(i) }
    if caps & QgsVectorDataProvider.AddAttributes:
        layer.dataProvider().changeAttributeValues({ feat.id() : attr })
    else:
        print("Not allowed")
    
layer.updateFields()

print('END')