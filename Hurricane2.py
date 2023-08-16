import folium
import pandas as pd
from folium.plugins import Draw
from folium.plugins import Search
from folium.plugins import MarkerCluster
df = pd.read_csv('../Datasets/atlantic.csv')
#view the dataset
print(df.head())

#Fixing time and date to much real-time
df["Time"] = df["Time"].astype("object")
time_replace = [str(x) for x in df["Time"].unique()]
for i, txt in enumerate(time_replace):
    time_replace[i] = txt.rjust(4, "0")
    time_replace[i] = f"{time_replace[i][0:2]}:{time_replace[i][2:4]}:00"
for old, new in zip(df["Time"].unique(), time_replace):
    df.loc[df["Time"]==old, "Time"] = new

df["Date"] = df["Date"].astype("object")
for i, date_str in enumerate(df["Date"].unique()):
    df.loc[df["Date"]==date_str, "Date"] = f"{str(date_str)[0:4]}-{str(date_str)[4:6]}-{str(date_str)[6:]}"

df["Datetime"] = df["Date"]+" "+df["Time"]
df["Datetime"] = pd.to_datetime(df["Datetime"])
df.drop(columns=["Date", "Time"], inplace=True)
df.sort_values(by=["Datetime"], inplace=True)

#Fixed the coordinates
def coordinate_mapping(x):
    coord = float(x[:-1])
    if x[-1]=="W":
        coord *= -1
    if x[-1]=="S":
        coord *= -1
    return coord

#Fixing the latitudes and longitudes
df["Latitude"] = df["Latitude"].apply(coordinate_mapping)
df["Longitude"] = df["Longitude"].apply(coordinate_mapping)

#Adjusting the lats and longs
df.loc[df.Longitude<-180, "Longitude"] = df.Longitude+360

#Adjusting the world map to the starting position
center = [30, -80]

#Create Map
map_kenya = folium.Map(location=center, zoom_start=5)
for index, df in df.iterrows():
    location = [df['Latitude'], df['Longitude']]
    #folium.Marker(location, popup = f'Name:{df["Name"]}\n Max Wind($):{df["Maximum Wind"]}').add_to(map_kenya)
    folium.CircleMarker(location, radius=5, popup=f'Hurricane:{df["Name"]}\n Date:{df["Datetime"]}', tooltip=None,).add_to(map_kenya)

#Draw function
draw = Draw()
draw.add_to(map_kenya)

marker_cluster = MarkerCluster().add_to(map_kenya)

search = Search(layer=marker_cluster, search_label="name", geom_type='Point',collapsed=False)
search.add_to(map_kenya)

# save map to html file
map_kenya.save('Hurricane2.html')