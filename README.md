# PythonPrj_2020
This project aims to examine the preference of the Greater white-fronted goose with regards to its habitat. We will use MODIS  500m land cover product and will overlay the raster file with the point shapefile that represents the stops of the geese along their tracks. We intend to show the preferred habitat(s) by creating a histogram with the dominant CLC classes. Finally, we want to create a map with the bird tracks, overlaid with Land Cover classification raster.

# RQ
What are the prefered stop-overs of the Greater white-fronted goose, based on Global Land Cover classification?

# Proposed Methodology
The methodological steps are listed below:
  -Acquire the data (Goose tracks shapefile + CLC raster).
  -Project all layers to the same CRS.
  -Crop raster to the extent of the shapefile.
  -Identify stop points.
  -Retrieve raster values on goose point locations.
  -Plot bar-chart to find what is the dominant CLC class.
  -Create a map of goose tracks.


# Libraray 
gdal, ogr os, numpy,and matplotlib

# Contributors
Eftychia Koukouraki, Mohammad Alasawedah, Muhammad Esmat Enan, Pablo Cruz

