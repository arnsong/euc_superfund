from os.path import dirname, join

import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (Button, ColumnDataSource, CustomJS, DataTable,
                          NumberFormatter, RangeSlider, TableColumn, Select,)

import config
import models as m

from sqlalchemy import select
from sqlalchemy.orm import Session

session = Session(bind=m.engine)

# Samples filtered on compound type
sql_df = pd.read_sql(session.query(m.SampleCompound).filter(m.SampleCompound.compound_id == 1).statement,
  con=m.engine)

samples_df = pd.read_sql(session.query(m.Sample, m.SampleCompound).\
  filter(m.Sample.id == m.SampleCompound.sample_id).filter(m.SampleCompound.compound_id==1).statement, con=m.engine)

source = ColumnDataSource(data=dict())
columns = []

source.data = samples_df
columns = [ TableColumn(field=column, title=column) for column in samples_df.columns ]

data_table = DataTable(source=source, columns=columns, width=1000, sizing_mode='stretch_width')

def update():

    df = samples_df
    
    columns = [ TableColumn(field=column, title=column) for column in df.columns ]
    
    data_table.source.data = df
    data_table.columns = columns

#select.on_change('value', lambda attr, old, new: update())

#button = Button(label="Download", button_type="success")
#button.js_on_click(CustomJS(args=dict(source=source),
#                            code=open(join(dirname(__file__), "download.js")).read()))

#controls = column(select, button)

curdoc().add_root(row(data_table))

update()
