from bokeh.models import (ColumnDataSource, 
                          GMapOptions, 
                          HoverTool,
                          ColorBar,
                          MultiSelect,
                          LogColorMapper, 
                          LogTicker)
from bokeh.models.formatters import PrintfTickFormatter
from bokeh.plotting import gmap, curdoc
from bokeh.transform import log_cmap
from bokeh.layouts import column, row
import colorcet as cc

import pandas as pd


# Import data from xlsx spreadsheet
data = pd.read_excel('/root/app/fish_contaminants_map/Lake_fish_tissue_study_location18Feb2021_updated.xlsx')

analytes = [ "MERCURY NG/G (ppb)", \
            "TOTAL DICHLORO BIPHENYLS NG/KG (ppt)", \
            "TOTAL HEPTACHLORO BIPHENYLS NG/KG (ppt)", \
            "TOTAL HEXACHLORO BIPHENYLS NG/KG (ppt)", \
            "TOTAL MONOCHLORO BIPHENYLS NG/KG (ppt)", \
            "TOTAL NONACHLORO BIPHENYLS NG/KG (ppt)", \
            "TOTAL OCTACHLORO BIPHENYLS NG/KG (ppt)", \
            "TOTAL PCBS NG/KG (ppt)", \
            "TOTAL PENTACHLORO BIPHENYLS NG/KG (ppt)", \
            "TOTAL TETRACHLORO BIPHENYLS NG/KG (ppt)", \
            "TOTAL TRICHLORO BIPHENYLS NG/KG (ppt)",\
            "TOTAL PCBS NG/G (ppb)"]


# Initialize Bokeh document, which will contain all of the models
doc = curdoc()

# Initialize multiselect widget that will allow the user to select the 
# analyte of interest for the map
multiselect = MultiSelect(value=["MERCURY NG/G (ppb)"], options=analytes, width=400, height=500)

# Initialize Google map basemap
gmap_key = "AIzaSyDfvhnKkOAhVDaM0Y4tcASqSJ1oJFUARW8"
analyte_map = gmap(gmap_key, 
                   GMapOptions(lat=40.2861, lng=-97.7394, map_type="roadmap", zoom=4), 
                   frame_width=800, frame_height=500)

# Filter fish data
map_data = data.loc[data[multiselect.value[0]], [ multiselect.value[0], 'Site_Name', 'Latitude', 'Longitude' ]]
map_data['analyte'] = multiselect.value[0]

source = ColumnDataSource(
    data=dict(analyte=map_data['analyte'],
              result=map_data[multiselect.value],
              lat=map_data['Latitude'],
              lon=map_data['Longitude'],
              site_id=map_data['Site_Name'])
)

# Add points to the map 
colors = log_cmap(field_name='result', palette=cc.fire,
            low=min(data.loc[:,multiselect.value[0]]), 
            high=max(data.loc[:,multiselect.value[0]]))

analyte_map.circle(x="lon", y="lat", size=10, line_color='white', fill_color=colors, fill_alpha=0.8, source=source)


# Add a color bar for scale to the map
color_mapper = LogColorMapper(palette=cc.fire, 
            low=max(0.001, min(data.loc[:,multiselect.value[0]])), 
            high=max(10, max(data.loc[:,multiselect.value[0]])))

color_bar = ColorBar(color_mapper=color_mapper, 
        label_standoff=10, 
        formatter=PrintfTickFormatter(format='%4.1e'),
        ticker=LogTicker(desired_num_ticks=4), 
        border_line_color=None, 
        orientation='vertical', 
        location=(40,0))
analyte_map.add_layout(color_bar, 'left')

# Add feature that displays the site information on mouse over
analyte_map.add_tools(HoverTool(
        tooltips=[("Site ID", "@site_id"),
                  ("Analyte", "@analyte"),
                  ("Result", "@result")],
        mode="mouse", point_policy="follow_mouse"
))

# Layout document
doc.add_root(row(column(multiselect, width=400), analyte_map))

# Function to update map based on selected analyte
def update():
    
    df = data.loc[data[multiselect.value[0]]>0, [ multiselect.value[0], 'Site_Name', 'Latitude', 'Longitude' ]]

    if df is not None:
        color_mapper.low = max(0.001, min(df.loc[:,multiselect.value[0]]))
        color_mapper.high = max(df.loc[:,multiselect.value[0]])

        df['analyte'] = multiselect.value[0]
        source.data = dict(analyte=df['analyte'],
                           result=df[multiselect.value[0]],
                           lat=df['Latitude'],
                           lon=df['Longitude'],
                           site_id=df['Site_Name'])
    else:
        source.data = dict(analyte=[],
                           result=[],
                           lat=[],
                           lon=[],
                           site_id=[])

multiselect.on_change('value', lambda attr, old, new: update())

update()
