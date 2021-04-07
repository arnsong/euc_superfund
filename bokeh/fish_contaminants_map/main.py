from bokeh.models import (ColumnDataSource, 
                          GMapOptions, 
                          HoverTool,
                          ColorBar,
                          MultiSelect)
from bokeh.models.formatters import PrintfTickFormatter
from bokeh.plotting import gmap, curdoc
from bokeh.layouts import column, row

import pandas as pd
import config

# Visualization components
class Map:

    def __init__(self): 

        # Initialize bokeh document
        self.doc = curdoc()

        # Load data
        self.data = pd.read_excel(config.DATAFILE)
        self.analytes = self.data.columns[11:-2].tolist()

        # Filter data
        self.map_data = self.filter_data(self.analytes[0], self.data)

        # Initialize multiselect widget that will allow the user to select the 
        # analyte of interest for the map
        self.multiselect = MultiSelect(value=[self.analytes[0]], options=self.analytes, width=400, height=500)
        self.multiselect.on_change('value', lambda attr, old, new: self.update())

        # Google Maps basemap
        self.map = gmap(config.GMAPS_API_KEY, 
                        GMapOptions(lat=40.2861, lng=-97.7394, map_type="roadmap", zoom=4), 
                        frame_width=800, frame_height=500)

        # Hover tool
        self.hovertool = self.map.add_tools(
                            HoverTool(tooltips=[("Site ID", "@site_id"),
                                                ("Analyte", "@analyte"),
                                                ("Result", "@result")],
                                      mode="mouse", point_policy="follow_mouse"))

        # Color mapper
        self.color_mapper = config.COLORMAPPER(palette=config.COLORMAP, 
                                               low=min(self.map_data[self.analytes[0]]), 
                                               high=max(self.map_data[self.analytes[0]]))
        
        # Data points
        self.source = ColumnDataSource(
            data = dict(analyte=self.map_data['analyte'],
                        result=self.map_data[self.analytes[0]],
                        lat=self.map_data['Latitude'],
                        lon=self.map_data['Longitude'],
                        site_id=self.map_data['Site_Name']))

        self.datapts = self.map.circle(x="lon", y="lat", 
                                       size=10, line_color='white', 
                                       fill_color={'field': 'result', 
                                                   'transform': self.color_mapper},
                                       fill_alpha=0.8, 
                                       source=self.source)

        # Color bar 
        self.color_bar = ColorBar(color_mapper=self.color_mapper, 
                                  label_standoff=10, 
                                  formatter=PrintfTickFormatter(format='%4.1e'),
                                  ticker=config.TICKER(desired_num_ticks=4), 
                                  border_line_color=None, 
                                  orientation='vertical', 
                                  location=(40,0))
        
        # Layout visualization
        # Add color bar to map rather than document.  It will be easier to control
        self.map.add_layout(self.color_bar, 'left')
        self.doc.add_root(row(column(self.multiselect, width=400), self.map))

    @staticmethod
    def filter_data(analyte, data):
        filtered_data = data.loc[:, [ analyte, 'Site_Name', 'Latitude', 'Longitude' ]].replace(' ', 'NaN')
        filtered_data[analyte] = filtered_data[analyte].astype('float')
        filtered_data = filtered_data.dropna()
        filtered_data['analyte'] = analyte

        return filtered_data

    def update(self):

        analyte = self.multiselect.value[0]
        map_data = self.filter_data(analyte, self.data)
        
        if map_data is not None:

            map_data['analyte'] = analyte

            self.color_mapper.low = min(map_data[analyte])
            self.color_mapper.high = max(map_data[analyte])
            self.source.data = dict(analyte=map_data['analyte'],
                                    result=map_data[analyte],
                                    lat=map_data['Latitude'],
                                    lon=map_data['Longitude'],
                                    site_id=map_data['Site_Name'])
        else:
            self.source.data = dict(analyte=[],
                                    result=[],
                                    lat=[],
                                    lon=[],
                                    site_id=[])


map = Map()
