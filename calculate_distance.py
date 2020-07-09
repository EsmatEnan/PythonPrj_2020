import os
from qgis.core import *
import qgis.utils
from datetime import datetime

# User inputs
data_dir = r"C:\Users\efthy\Documents\MasterGeoTech\semester2\Python\Project\data"
shape_file = os.path.join(data_dir, 'goose', 'points_reprojected.shp')

def getColumnValues(layer, field):
    values = []
    try:
        features = layer.getFeatures()
        for feature in features:
            values.append(feature.attribute(str(field)))
    except Exception as e:
        print("Function getColumnValues failed, because", e)
    return values

def addFieldtoLayer(field_name, field_type):
    # Adding a field (attribute)
    if caps & QgsVectorDataProvider.AddAttributes:
        res = layer.dataProvider().addAttributes([QgsField(field_name, field_type)])
    print(res)
    layer.updateFields()

    fields = layer.fields()
    field_idx = fields.indexFromName(field_name)
    print(field_idx)
    return field_idx

def calculateDistance(item1, item2):
    current_feat = layer.getFeature(item1)
    prv_feat = layer.getFeature(item2)
    point1 = QgsPoint(current_feat.attribute('utm_east'), current_feat.attribute('utm_north'))
    point2 = QgsPoint(prv_feat.attribute('utm_east'), prv_feat.attribute('utm_north'))
    distance = point1.distance(point2)
    attr = { distance_idx : distance }
    return { current_feat.id() : attr }

def calculateTimeInterval(item1, item2, attr_key):
    tdelta = datetime.strptime(item1, datetime_format) - datetime.strptime(item2, datetime_format)
    attr = { time_interval_idx : str(tdelta) }
    return { dict_sorted[i][0] : attr }

layer = iface.addVectorLayer(shape_file, "shape:", "ogr")

if not layer:
    print("Shapefile failed to load!")

# Check for editing rights (capabilities)
caps = layer.dataProvider().capabilities()

distance_idx = addFieldtoLayer("dist_prv", QVariant.Double)
time_interval_idx = addFieldtoLayer("interv_prv", QVariant.String)
#speed_idx = addFieldtoLayer("km_p_h", QVariant.Double)

values = getColumnValues(layer, 'ind_ident')
unique_values = list(set(values))

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
            #print("i=0")
            continue
        dist = calculateDistance(dict_sorted[i][0], dict_sorted[i-1][0])
        time_interval = calculateTimeInterval(dict_sorted[i][1], dict_sorted[i-1][1], dict_sorted[i][0])
        if caps & QgsVectorDataProvider.AddAttributes:
            layer.dataProvider().changeAttributeValues(dist)
            layer.dataProvider().changeAttributeValues(time_interval)
        else:
            print("Not allowed")
    
    layer.updateFields()

print('END')
