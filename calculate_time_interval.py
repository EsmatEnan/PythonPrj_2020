import os
from qgis.core import *
import qgis.utils
from datetime import datetime

def getColumnValues(layer, field):
    values = []
    try:
        features = layer.getFeatures()
        for feature in features:
            values.append(feature.attribute(str(field)))
    except Exception as e:
        print("Function getColumnValues failed, because", e)
    return values


# path to shapefile we want to add the new field
data_dir = r"C:\Users\efthy\Documents\MasterGeoTech\semester2\Python\Project\data"
shape_file = os.path.join(data_dir, 'goose', 'points_reprojected.shp')

layer = iface.addVectorLayer(shape_file, "shape:", "ogr")

if not layer:
    print("Shapefile failed to load!")

values = getColumnValues(layer, 'ind_ident')
unique_values = list(set(values))

# Check for editing rights (capabilities)
caps = layer.dataProvider().capabilities()

# Adding a field (attribute)
if caps & QgsVectorDataProvider.AddAttributes:
    res = layer.dataProvider().addAttributes([QgsField("interv_prv", QVariant.String)])
print(res)
layer.updateFields()

fields = layer.fields()
field_idx = fields.indexFromName('interv_prv')
print(field_idx)

datetime_format = "%Y-%m-%d %H:%M:%S"

for bird in unique_values:
    print(bird)
    dict = {}
    for feat in layer.getFeatures():
        if (feat.attribute('ind_ident') == bird):
            #create list here
            dict[feat.id()] =  feat.attribute('timestamp')
    #sort it
    dict_sorted = sorted(dict.items(), key=lambda x: x[1]) # creates list of tuples
    for i in range( len(dict_sorted) ):
        if (i == 0):
            print("i=0")
            continue
        time1 = dict_sorted[i][1]
        time2 = dict_sorted[i-1][1]
        tdelta = datetime.strptime(time1, datetime_format) - datetime.strptime(time2, datetime_format)
#        print(tdelta)

        attr = { field_idx : str(tdelta) }
        if caps & QgsVectorDataProvider.AddAttributes:
            layer.dataProvider().changeAttributeValues({ dict_sorted[i][0] : attr })
        else:
            print("Not allowed")
    
    layer.updateFields()

print('END')
