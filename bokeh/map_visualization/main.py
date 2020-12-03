import json
import pandas as pd

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool, CustomJS, MultiSelect, ColorBar, LinearColorMapper
from bokeh.plotting import gmap
from bokeh.palettes import Spectral11
from bokeh.transform import linear_cmap
from bokeh.layouts import column, row
import matplotlib as mpl
import os
from bokeh.plotting import curdoc, figure

doc = curdoc()

fish_data = pd.read_csv('/root/app/data/NCCA/ncca2010_ecological_fish_tissue_contaminant_data.csv')
location_data = pd.read_csv('/root/app/data/NCCA/assessed_ncca2010_siteinfo.revised.06212016.csv')

fish_data['LAT_DD'] = None
fish_data['LON_DD'] = None

for index, datarow in location_data.iterrows():
    fish_data.loc[fish_data['SITE_ID']==datarow['SITE_ID'],'LAT_DD'] = datarow['ALAT_DD']
    fish_data.loc[fish_data['SITE_ID']==datarow['SITE_ID'],'LON_DD'] = datarow['ALON_DD']

output_file("gmap.html")

OPTIONS = list(set(fish_data.loc[fish_data['PARAMETER_CAT']=='PCB', 'PARAMETER']))
OPTIONS.sort()
multi_select = MultiSelect(options=OPTIONS, height=500)

map_options = GMapOptions(lat=40.2861, lng=-97.7394, map_type="roadmap", zoom=4)

# Filter fish data on 
map_data = fish_data.loc[(fish_data['PARAMETER']=='PCB141') & (fish_data['RESULT']>0), 
                         ['SITE_ID', 'LAT_DD', 'LON_DD', 'PARAMETER', 'RESULT', 'UNITS']]

# For GMaps to function, Google requires you obtain and enable an API key:
#
#     https://developers.google.com/maps/documentation/javascript/get-api-key
#
# Replace the value below with your personal API key:
p = gmap("AIzaSyDfvhnKkOAhVDaM0Y4tcASqSJ1oJFUARW8", map_options, title="NCCA data", frame_width=800, frame_height=500)


source = ColumnDataSource(
    data=dict(lat=map_data['LAT_DD'],
              lon=map_data['LON_DD'],
              site_id=map_data['SITE_ID'],
              parameter=map_data['PARAMETER'],
              result=map_data['RESULT'],
              units=map_data['UNITS'])
)

p.add_tools(HoverTool(
    tooltips=[("Site ID", "@site_id"), 
              ("Parameter", "@parameter"),
              ("Result", "@result @units")],
    mode="mouse", point_policy="follow_mouse"
))

colors = linear_cmap(field_name='result', palette=Spectral11, low=min(map_data['RESULT']), high=max(map_data['RESULT']))
color_mapper = LinearColorMapper(palette=Spectral11, low=min(map_data['RESULT']), high=max(map_data['RESULT']))
color_bar = ColorBar(color_mapper=color_mapper, border_line_color=None)

p.circle(x="lon", y="lat", size=10, line_color='white', fill_color=colors, fill_alpha=0.8, source=source)

def select_data():

    if len(multi_select.value)>0:
        map_data = fish_data.loc[(fish_data['PARAMETER']==multi_select.value[0]) & (fish_data['RESULT']>0), 
                                 ['SITE_ID', 'LAT_DD', 'LON_DD', 'PARAMETER', 'RESULT', 'UNITS']]

        return map_data
    else:
        return None
    
def update():

    df = select_data()
    
    if df is not None:
        source.data = dict(lat=df['LAT_DD'],
            lon=df['LON_DD'],
            site_id=df['SITE_ID'],
            parameter=df['PARAMETER'],
            result=df['RESULT'],
            units=df['UNITS'])
        gmap.title = df['PARAMETER']

multi_select.on_change('value', lambda attr, old, new: update())

doc.add_root(row(column(multi_select, width=200), p))
doc.title = "NCCA data map visualization"

update()
