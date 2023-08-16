import plotly.express as px
import pandas as pd

us_cities = pd.read_csv("us-cities-top-1k.csv")
atlantic_weather = pd.read_csv("atlantic_clean.csv", parse_dates=[2])


# Cat 1 = 74-95 MPH
# Cat 2 = 96-110 MPH
# Cat 3 = 111-130 MPH
# Cat 4 = 131-155 MPH
# Cat 5 = 155+
def clean_data(df):
    cat_list = []
    for i, lat in enumerate(df["Latitude"]):
        cat = 0
        df["Date"] = df["Date"]
        lat_neg = 1
        long_neg = 1
        long = atlantic_weather["Longitude"][i]
        if "S" in lat:
            lat_neg = -1
        if "W" in long:
            long_neg = -1
        lat = lat.replace("W", "")
        lat = lat.replace("N", "")
        lat = lat.replace("E", "")
        lat = lat.replace("S", "")
        long = long.replace("N", "")
        long = long.replace("W", "")
        long = long.replace("S", "")
        long = long.replace("E", "")
        df["Latitude"][i] = float(lat) * lat_neg
        df["Longitude"][i] = float(long) * long_neg
        if df["Maximum Wind"][i] < 0:
            df["Maximum Wind"][i] = 0
        if df["Maximum Wind"][i] < 95:
            cat = 1
        elif df["Maximum Wind"][i] < 110:
            cat = 2
        elif df["Maximum Wind"][i] < 131:
            cat = 3
        elif df["Maximum Wind"][i] < 155:
            cat = 4
        else:
            cat = 5
        cat_list.append(cat)
        if df["Minimum Pressure"][i] < 0:
            df["Minimum Pressure"][i] = 1013
    df["Category"] = cat_list


def filter_wind(df, min_speed):
    for i, wind in enumerate(df["Maximum Wind"]):
        if wind < min_speed:
            df.drop(i, inplace=True)


def filter_event(df, e="L"):
    for i, event in enumerate(df["Event"]):
        if str(event).strip() == "L":
            1 == 1
        else:
            df.drop(i, inplace=True)


def filter_events(df, e=["L"]):
    for i, event in enumerate(df["Event"]):
        if str(event).strip() in e:
            1 == 1
        else:
            df.drop(i, inplace=True)


def filter_name(df, name):
    for i, name_t in enumerate(df["Name"]):
        if not name_t.strip() == name:
            df.drop(i, inplace=True)


# clean_data(atlantic_weather)
# atlantic_weather.to_csv("atlantic_clean.csv")
atlantic_weather = pd.read_csv("atlantic_clean.csv", parse_dates=[2])
filter_wind(atlantic_weather, 90)
# filter_name(atlantic_weather,"FAY")
# filter_event(atlantic_weather,"L")


# fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig = px.scatter_mapbox(atlantic_weather, lat="Latitude", lon="Longitude", hover_name="Name",
                        hover_data=["Status", "Date", "Maximum Wind"], color="Maximum Wind", zoom=3, height=300,
                        opacity=.5)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.write_html("map.html")
fig.show()