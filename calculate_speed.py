import os
from qgis.core import *
import qgis.utils

def convertTimeStringToHours(input_string):
    hours = 0
    if ("day" in input_string):
        hours = 24*int(input_string[0])
        input_string = input_string.split(', ')[1]
    hours = hours + int(input_string.split(':', 1)[0])
    print(hours)
    return hours

# path to shapefile we want to add the new field
data_dir = r"C:\Users\efthy\Documents\MasterGeoTech\semester2\Python\Project\data"
shape_file = os.path.join(data_dir, 'goose', 'points_reprojected.shp')

layer = iface.addVectorLayer(shape_file, "shape:", "ogr")

if not layer:
    print("Shapefile failed to load!")

## Check for editing rights (capabilities)
caps = layer.dataProvider().capabilities()

# Adding a field (attribute)
if caps & QgsVectorDataProvider.AddAttributes:
    res = layer.dataProvider().addAttributes([QgsField("km_p_h", QVariant.Double)])
print(res)
layer.updateFields()

fields = layer.fields()
field_idx = fields.indexFromName('km_p_h')
print(field_idx)

for feat in layer.getFeatures():
    distance = feat.attribute('dist_prv')
    time = feat.attribute('interv_prv')
    if (distance and time not in [None, "", "NULL", 0]):
        print(distance, time)
        speed = (distance/1000) / convertTimeStringToHours(time)
        attr = { field_idx : speed }
        if caps & QgsVectorDataProvider.AddAttributes:
            layer.dataProvider().changeAttributeValues({ feat.id() : attr })
        else:
            print("Not allowed")
    
layer.updateFields()

print('END')