from bokeh.models import (ColumnDataSource, 
                          GMapOptions, 
                          HoverTool,
                          ColorBar,
                          MultiSelect,
                          LogColorMapper, 
                          LogTicker)
from bokeh.models.formatters import PrintfTickFormatter
from bokeh.plotting import gmap, curdoc
from bokeh.transform import linear_cmap
from bokeh.layouts import column, row
import colorcet as cc

import pandas as pd

# Import data from xlsx spreadsheet
data = pd.read_excel('/root/app/fish_contaminants_map/Lake_fish_tissue_study_location_5Mar2021.xlsx')

analytes = [ "Mercury ng/g (ppb)", \
            "Total dichloro biphenyls ng/g (ppb)", \
            "Total heptachloro biphenyls ng/g (ppb)", \
            "Total hexachloro biphenyls ng/g (ppb)", \
            "Total monochloro biphenyls ng/g (ppb)", \
            "Total nonachloro biphenyls ng/g (ppb)", \
            "Total octachloro biphenyls ng/g (ppb)", \
            "Total PCBs ng/g (ppb)", \
            "Total pentachloro biphenyls ng/g (ppb)", \
            "Total tetrachloro biphenyls ng/g (ppb)", \
            "Total trichloro biphenyls ng/g (ppb)" ]

# Initialize Bokeh document, which will contain all of the models
doc = curdoc()

# Initialize multiselect widget that will allow the user to select the 
# analyte of interest for the map
multiselect = MultiSelect(value=["Mercury ng/g (ppb)"], options=analytes, width=400, height=500)

# Initialize Google map basemap
gmap_key = "AIzaSyDfvhnKkOAhVDaM0Y4tcASqSJ1oJFUARW8"
analyte_map = gmap(gmap_key, 
                   GMapOptions(lat=40.2861, lng=-97.7394, map_type="roadmap", zoom=4), 
                   frame_width=800, frame_height=500)

# Filter fish data
analyte = multiselect.value[0]
map_data = data.loc[:, [ analyte, 'Site_Name', 'Latitude', 'Longitude' ]].replace(' ', 'NaN')
map_data[analyte] = map_data[analyte].astype('float')
map_data = map_data.dropna()
map_data['analyte'] = multiselect.value[0]

# Remove rows with missing values
map_data = map_data.dropna()

source = ColumnDataSource(
    data = dict(analyte=map_data['analyte'],
                result=map_data[multiselect.value[0]],
                lat=map_data['Latitude'],
                lon=map_data['Longitude'],
                site_id=map_data['Site_Name'])
)

# Add a color bar for scale to the map
color_mapper = LogColorMapper(palette=cc.CET_L17, 
            low=min(map_data[multiselect.value[0]]), 
            high=max(map_data[multiselect.value[0]]))

circles = analyte_map.circle(x="lon", y="lat", size=10, line_color='white', 
                            fill_color={'field': 'result', 'transform': color_mapper},
                            fill_alpha=0.8, source=source)

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
    
    analyte = multiselect.value[0]
    df = data.loc[:, [analyte, 'Site_Name', 'Latitude', 'Longitude' ]].replace(' ', 'NaN')
    df[analyte] = df[analyte].astype('float')
    df = df.dropna()
    
    if df is not None:

        color_mapper.low = min(df[analyte])
        color_mapper.high = max(df[analyte])

        df['analyte'] = analyte

        source.data = dict(analyte=df['analyte'],
                           result=df[analyte],
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
