import pandas as pd
import ogr

#user input
in_file = r"E:\Munster\python\final project\movebank\goose\outputs\pointsPrj.shp"

# create codes & classes serieses
codes = pd.Series(range(1,21))
classes = pd.Series({0:'Broadleaf Evergreen Forest',1:'Broadleaf Deciduous Forest',
                     2:'Needleleaf Evergreen Forest',3:'Needleleaf Deciduous Forest',
                     4:'Mixed Forest',5:'Tree Open',6:'Shrub',7:'Herbaceous',
                     8:'Tree/Shrub',9:'Sparse vegetation',
                     10:'Cropland',11:'Paddy field',12:'Cropland/Other Vegetation Mosaic',13:'Mangrove',
                     14:'Wetland',15:'gravel,rock',16:'sand',17:'Urban',
                     18:'Snow/Ice',19:'Water bodies'

})

#combine the two serieses in one dataframe
landcover = pd.DataFrame({'code': codes,'land cover': classes})

#open the track shape file
ds=ogr.Open(in_file,1)
lyr=ds.GetLayer(0)

# Add a new field
new_field = ogr.FieldDefn('Land cover', ogr.OFTString)
lyr.CreateField(new_field)

#Itrate over the shapfile features
for feat in lyr:
    int_value = feat['VALUE']
    for i in landcover.index:
        if int_value == landcover.loc[i,'code']:
            land_cover = landcover.loc[i,'land cover']
            feat.SetField('land cover', land_cover)
            lyr.SetFeature(feat)
    
# Close the Shapefile
ds = None




