import os
import folium, vincent
import pandas as pd
import calendar,datetime

def popup_chart(station):
    months = [i+1 for i in xrange(12)]
    mins = list(station[[str(num)+'_tmin' for num in months]])
    maxes = list(station[[str(num)+'_tmax' for num in months]])
    avgs = list(station[[str(num)+'_tavg' for num in months]])

    weather_frame = pd.DataFrame({"Min":mins, "Max":maxes, "Average":avgs, "month": months}).set_index("month")

    chart = vincent.Line(weather_frame)
    chart.axis_titles(x=station['name']+", "+station["country"],y="Temp (C)")
    chart.legend(title="Key")
    chart.width=400
    chart.height=200
    chart.title=station['name']+", "+station["country"]
    chart.padding={'top':20,'right':80,'bottom':40,'left':40}

    chart.to_json("viz/data_{0}.json".format(station['id']))
    return chart

f_map = folium.Map(
    location=[0,0],
    zoom_start=2,
    tiles="Mapbox Bright")

data = pd.read_csv("data/csv/categories.csv")

cat_colors=['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a']

for category,color in zip(data['category'].unique(),cat_colors):
    for _,station in data[data.category == category].dropna().iterrows():
        f_map.polygon_marker([station['lat'],station['long']], 
            radius=5, 
            popup=(popup_chart(station),"data_{0}.json".format(station['id'])),
            line_color=None,
            fill_color=color, 
            fill_opacity=1)

f_map.create_map(path='viz/map.html')