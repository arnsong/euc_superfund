from os.path import dirname, join

import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (Button, ColumnDataSource, CustomJS, DataTable,
                          NumberFormatter, RangeSlider, TableColumn, Select,)


datafiles = { 
              'Dartmouth': ['dartmouth/sediment_individual.csv'],
              'Duke': ['duke/mercury_analysis.csv'],
              'Smithsonian': ['smithsonian/chesapeake_marsh.csv']
            }

source = ColumnDataSource(data=dict())
columns = []

select = Select(title="Data source:", value="Dartmouth", options=["Dartmouth", "Duke", "Smithsonian"])

data_table = DataTable(source=source, columns=columns, width=1000, autosize_mode='fit_viewport')

def update(attr, old, new):

    fname = join(dirname(__file__), datafiles[select.value][0])
    df = pd.read_csv(fname)
    
    columns = [ TableColumn(field=column, title=column) for column in df.columns ]
    
    data_table.source.data = df
    data_table.columns = columns

select.on_change('value', update)

button = Button(label="Download", button_type="success")
button.js_on_click(CustomJS(args=dict(source=source),
                            code=open(join(dirname(__file__), "download.js")).read()))

controls = column(select, button)

curdoc().add_root(row(controls, data_table))
curdoc().title = "Export CSV"

update()
