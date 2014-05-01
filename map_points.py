import os
import folium, vincent
import pandas as pd
import calendar

def popup_chart(station):
    mins = list(station[[str(num+1)+'_tmin' for num in xrange(12)]])
    maxes = list(station[[str(num+1)+'_tmax' for num in xrange(12)]])
    avgs = list(station[[str(num+1)+'_tavg' for num in xrange(12)]])
    
    months = [calendar.month_name[i+1] for i in range(12)]
    
    test = pd.DataFrame({"Min":mins, "Max":maxes, "Average":avgs})
    chart = vincent.Line(test)
    chart.axis_titles(x='Month',y="Temp (C)")
    chart.legend(title="Temperature")
    chart.width=400
    chart.height=200
    chart.to_json("viz/data_{0}.json".format(station['id']))
    chart.title=station['name']+", "+station["country"]
    return chart

f_map = folium.Map(
    location=[0,0],
    zoom_start=2,
    tiles="Mapbox Bright")

data = pd.read_csv("data/csv/categories.csv")

cat_colors=['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a']

for category,color in zip(data['category'].unique(),cat_colors):
    # for _,station in data[data.category == category].iterrows():
    for _,station in data[data.category == category].head(5).iterrows():
        vis = vincent.Bar([10, 20, 30, 40, 30, 20])
        # vis.tabular_data()
        vis.to_json('viz/vis.json')
        # map.polygon_marker(location=[45.5, -122.5], popup=(vis, 'vis.json'))

        f_map.polygon_marker([station['lat'],station['long']], 
            radius=5, 
            # popup=station['name']+", "+station["country"], 
            popup=(popup_chart(station),"data_{0}.json".format(station['id'])),
            # popup = (vis, 'vis.json'),
            line_color=None,
            fill_color=color, 
            fill_opacity=1)

os.remove('viz/map.html')
f_map.create_map(path='viz/map.html')