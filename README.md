# Python Project 2020
This project aims to examine the preference of the Greater white-fronted goose with regards to the land cover class at the stopover sites during migration. We will use MODIS  500m land cover product and will overlay the raster file with the point shapefile that represents the stops of the geese along their tracks. In order to study the preferred land cover class(es), we have created a series of tools, for data pre-processing, analysis and visualization.

# RQ
What are the prefered stop-overs of the Greater white-fronted goose, based on Global Land Cover classification?

# How to use the Tools
The tools we have created require to have the Land Cover raster and the GPS track of the geese on your own filesystem. The file/directory paths or any other variables that can be considered as "input" in our system can be defined at the very beginning of the script tool.

## More specifically:
* change_projection.py -> Projects the shapefile to the same CRS as the raster. The inputs are the shapefile and the raster and the output is a new reprojected shapefile.
* crop_raster.py -> Crops the raster to the extent of the shapefile, plus a small buffer. The inputs are the shapefile, the raster and the buffer size in degrees. The output is the cropped raster.
* add_distance_speed_fields.py -> Calculates the distance, time interval and speed between a track point and the previous one. The input is the shapefile and the output is the same shapefile with the 3 calculated fields.
* identify_stopover.py -> Identifies which of the track points can be considered stopovers. The input is the shapefile and the output is a new shapefile that contains only the stopover points.
* retrieve_raster_values.py -> Retrieves raster values on shapefile point locations. The inputs are the shapefile and the raster and the output is the same shapefile with one more field in the attribute table.
* translate_landcover_class.py -> Translates the land cover class code to land cover class name. The input is the shapefile and the output is the same shapefile with one more field in the attribute table.
* create_pie_chart.py -> Creates 2 pie charts, one for all track points and one only for stopovers. The inputs are the shapefile with all track points and the shapefile with the stopovers only and the outputs are 2 pie charts.
* create_bar_chart.py -> Creates a bar chart. The inputs are the shapefile to be used, the field for which the bar chart will be created, the title of the chart and a boolean variable for translating the land cover class code to name. Disabling this variable can make the tool script work in other cases, too. The output is a bar chart.
* map_stopovers.py -> Creates a map of goose stopovers. The inputs are the shapefile and the raster and the output is a map.


# Libraries 
gdal/ogr, osr, pyqgis, numpy, matplotlib

# Contributors
Eftychia Koukouraki, Mohammad Alasawedah, Muhammad Esmat Enan, Pablo Cruz

