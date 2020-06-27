import pandas as pd
import ogr
from matplotlib import pyplot as plt

#open the track shape file
in_file = r"E:\Munster\python\final project\movebank\goose\outputs\pointsPrj.shp"
ds=ogr.Open(in_file,1)
lyr=ds.GetLayer(0)

# put all landcover classes in a list
class_list = []
for feat in lyr:
    classes = feat['land cover']
    class_list.append(classes)

# count the occurance of each lancover class and put it in a dictionary
class_dic = dict((x,class_list.count(x)) for x in set(class_list))

labels = class_dic.keys()
x_tics = range(len(class_dic))

f, axarr = plt.subplots(1, figsize=(5,8))
one = axarr.bar(x_tics , class_dic.values(), align='center')
plt.xticks( x_tics, labels , rotation='vertical')
f.suptitle('Land cover for the study area')
plt.subplots_adjust(bottom=0.30)
plt.show()

# Close the Shapefile
ds = None
    