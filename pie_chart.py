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
    classes = feat['landcover']
    class_list.append(classes)

# put all landcover classes for stopover points in a list
class_list1 = []
print (class_list1)
for feat in lyr1:
    classes1 = feat['landcover']
    class_list1.append(classes1)



# count the occurance of each lancover class in all points and put it in a dictionary
class_dic = dict((x,class_list.count(x)) for x in set(class_list))
print(class_dic)

# count the occurance of each lancover class in stopover points and put it in a dictionary
class_dic1 = dict((x1,class_list1.count(x1)) for x1 in set(class_list1))
print(class_dic1)

# create pie charts 
#Get the labels (class names)
allpoints_labels = class_dic.keys()
stopover_labels =  class_dic1.keys()

# to make the color cycle more than 15 colors & use the same color for the two charts
colors = {'red', 'blue','yellow','green', 'orange',
          'goldenrod', 'gold','aqua','violet',
          'pink','gray', 'lawngreen',
          'teal', 'cadetblue', 'lightgreen'}


# create pie charts for fly points
f1= plt.figure( figsize=(5,8))
plt.pie(class_dic.values(), colors=colors, startangle=90)
f1.suptitle('Land cover for the fly points')
legend1 = plt.legend(allpoints_labels, loc="right")
plt.axis('equal')

# create pie charts for stopover points
f2 = plt.figure(figsize=(5,8))
plt.pie(class_dic1.values(), colors=colors, startangle=90)
f2.suptitle('Land cover for the stopover sites')
legend2 = plt.legend(stopover_labels, loc="right")
plt.axis('equal')


plt.show()




# Close the Shapefile
ds = None
ds1 = None
