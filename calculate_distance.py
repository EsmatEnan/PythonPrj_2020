import os
from qgis.core import *
import qgis.utils

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
#print(unique_values)

# Check for editing rights (capabilities)
caps = layer.dataProvider().capabilities()

# Adding a field (attribute)
if caps & QgsVectorDataProvider.AddAttributes:
    res = layer.dataProvider().addAttributes([QgsField("dist_nxt", QVariant.Double)])
print(res)
layer.updateFields()

fields = layer.fields()
field_idx = fields.indexFromName('dist_nxt')
print(field_idx)

for bird in unique_values:
    print(bird)
    dict = {}
    for feat in layer.getFeatures():
        if (feat.attribute('ind_ident') == bird):
            #create list here
            dict[feat.id()] =  feat.attribute('timestamp')
    #sort it
    dict_sorted = sorted(dict.items(), key=lambda x: x[1]) # creates list of tuples
    #print(dict)
    #print(dict_sorted)
    for i in range( len(dict_sorted) -1 ):
        #print(dict_sorted[i][1], dict_sorted[i+1][1])
        current_feat = layer.getFeature(dict_sorted[i][0])
        next_feat = layer.getFeature(dict_sorted[i+1][0])
        #print(current_feat['utm_east'], current_feat['utm_north'])
        point1 = QgsPoint(current_feat.attribute('utm_east'), current_feat.attribute('utm_north'))
        point2 = QgsPoint(next_feat.attribute('utm_east'), next_feat.attribute('utm_north'))
        #print(point1, point2)
        distance = point1.distance(point2)
        #print(distance)
        attr = { field_idx : distance }
        if caps & QgsVectorDataProvider.AddAttributes:
            layer.dataProvider().changeAttributeValues({ current_feat.id() : attr })
        else:
            print("Not allowed")
    
    layer.updateFields()

print('END')
