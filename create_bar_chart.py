import pandas as pd
import ogr
from matplotlib import pyplot as plt

# important inputs: data directory, input shapefile, attribute to create bar-graph for, enable translation and title
data_dir = r"C:\Users\efthy\Documents\MasterGeoTech\semester2\Python\Project\data"
in_file = os.path.join(data_dir, 'goose', 'stopovers.shp')
attribute = 'VALUE'
enable_translation = True
title = 'Land cover for the stopover points'

# translateValues: Translates land cover classes from number to string descriptions.
# Input args
# * int_number: the number corresponding to the class (int from 1 to 20)
# * bool_translate: on True translate number to description (boolean)
# Returns
# The class description if bool_translate is True on Success, otherwise returns the input
def translateValues(int_number, bool_translate=False):
    numbers = list(range(1, 21))
    names = ["Broadleaf Evergreen Forest", "Broadleaf Deciduous Forest", 
    "Needleleaf Evergreen Forest", "Needleleaf Deciduous Forest", "Mixed Forest", 
    "Tree Open", "Shrub", "Herbaceous", "Herbaceous with Sparse Tree/Shrub", 
    "Sparse vegetation", "Cropland", "Paddy field", "Cropland/Other Vegetation Mosaic", 
    "Mangrove", "Wetland", "Bare area,consolidated(gravel,rock)", 
    "Bare area,unconsolidated (sand)", "Urban", "Snow / Ice", "Water bodies"]
    dictionary = dict(zip(numbers, names))
    if (bool_translate == True):
    	return dictionary[int_number]
    else:
    	return int_number
    

#open the track shape file
ds=ogr.Open(in_file,1)
lyr=ds.GetLayer(0)

# put all landcover classes in a list
class_list = []
for feat in lyr:
    classes = feat[attribute]
    class_list.append(translateValues(classes, enable_translation))

# count the occurance of each lancover class and put it in a dictionary
class_dic = dict((x,class_list.count(x)) for x in set(class_list))

labels = class_dic.keys()
x_tics = range(len(class_dic))

f, axarr = plt.subplots(1, figsize=(5,8))
one = axarr.bar(x_tics , class_dic.values(), align='center')
plt.xticks( x_tics, labels , rotation='vertical')
f.suptitle(title)
plt.subplots_adjust(bottom=0.30)
plt.show()

# Close the Shapefile
ds = None
    