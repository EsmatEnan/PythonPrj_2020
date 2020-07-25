import pandas as pd
import ogr
from matplotlib import pyplot as plt

#open the track shape file
all_points = r"E:\Munster\python\final project\movebank\goose\outputs\pointsPrj.shp"
ds=ogr.Open(all_points,1)
lyr=ds.GetLayer(0)


#open the stopover shape file
stop_points = r"E:\Munster\python\final project\movebank\goose\outputs\stopovers3.shp"
ds1=ogr.Open(stop_points,1)
lyr1=ds1.GetLayer(0)

# put all landcover classes for all points in a list
class_list = []
for feat in lyr:
    classes = feat['landss']
    class_list.append(classes)

# put all landcover classes for stopover points in a list
class_list1 = []
print (class_list1)
for feat in lyr1:
    classes1 = feat['landss']
    class_list1.append(classes1)



# count the occurance of each lancover class in all points and put it in a dictionary
class_dic = dict((x,class_list.count(x)) for x in set(class_list))

# count the occurance of each lancover class in stopover points and put it in a dictionary
class_dic1 = dict((x1,class_list1.count(x1)) for x1 in set(class_list1))

# create pie charts 
#Get the labels (class names)
allpoints_labels = class_dic.keys()
stopover_labels =  class_dic1.keys()

#create color dictionary to use the same color for the the charts and the same in the final map
dic_color = {'Cropland': 'violet', 'Wetland': 'teal',
             'Needleleaf Evergreen Forest': 'orange',
             'Needleleaf Deciduous Forest': 'green',
             'Shrub': 'gold', 'Water bodies': 'blue',
             'Paddy field': 'sienna',
             'Cropland/Other Vegetation Mosaic': 'lightgreen',
             'Sparse vegetation': 'forestgreen',
             'Herbaceous': 'darkred',
             'Broadleaf Deciduous Forest': 'yellow',
             'Mixed Forest': 'red',
             'Urban': 'rosybrown','Tree Open': 'gray',
             'Broadleaf Evergreen Forest': 'lightblue'}

# create pie charts for fly points
f1= plt.figure( figsize=(5,8))
## a percentage label when it is more than 2%
def autopct(pct):
    return ('%1.1f%%' % pct) if pct > 2 else ''

## retrive the patch widges & texts of the plot
fly_widges = plt.pie(class_dic.values(),labels = allpoints_labels,autopct=autopct,startangle=90,labeldistance=1.05)
## change the color of each class depend on the color dictionary  
for fly_widge in fly_widges[0]:
    fly_widge.set_facecolor(dic_color[fly_widge.get_label()])
## hide the labels of each class on the chart to avoid the overlapping labels
for fly_widge_text in fly_widges[1]:
    fly_widge_text.set_text(' ')



## set title & legend
f1.suptitle('Land cover for the fly points')
legend1 = plt.legend(allpoints_labels, loc="right")
plt.axis('equal')


# create pie charts for stopover points
f2 = plt.figure(figsize=(5,8))

# retrive the patch widges & texts of the plot
stop_widges = plt.pie(class_dic1.values(),labels = stopover_labels,autopct='%1.1f%%',startangle=90)
## change the color of each class depend on the color dictionary
for stop_widge in stop_widges[0]:
    stop_widge.set_facecolor(dic_color[stop_widge.get_label()])
## hide the labels of each class on the chart to avoid the overlapping labels
for stop_widge_text in stop_widges[1]:
    stop_widge_text.set_text(' ')


    
## set title & legend
f2.suptitle('Land cover for the stopover sites')
legend2 = plt.legend(stopover_labels, loc="right")
plt.axis('equal')


plt.show()


# Close the Shapefile
ds = None
ds1 = None
