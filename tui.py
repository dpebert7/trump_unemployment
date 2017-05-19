# To run from command line: bokeh serve --show tui.py

import pandas as pd
import numpy as np
from datetime import datetime
#from datetime import datetime as dt
#from bokeh import events
from bokeh.layouts import column#, row, widgetbox
from bokeh.models import HoverTool, Legend
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Circle
from bokeh.io import show, curdoc, vform
from bokeh.models.annotations import Span, Label
from bokeh.models.widgets import TextInput, Button, Paragraph, Select, Slider
from bokeh.models.callbacks import CustomJS

#from bokeh.io import output_notebook, show

df = pd.read_csv("data.csv")
df['date_formatted']=df['date'].astype('datetime64[ns]')
df.dtypes
#print(df)


# Import Data
start_date = '2015-06-01'
graph_data = df.loc[df['date_formatted'] >= start_date]
graph_data.index = pd.DatetimeIndex(graph_data['date'])
graph_data['date_string'] = graph_data['date'].astype(str)
graph_data['trump_unemployment'] = graph_data['trump_unemployment'].round()
#print(graph_data)
#print(graph_data.loc[1,1])

# Set Up Data
time_series = graph_data.index.T
fed_series = np.array(graph_data['fed_unemployment']).astype(np.double)
fedmask = np.isfinite(fed_series)

trump_min_series = np.array(graph_data['trump_min']).astype(np.double)
trumpminmask = np.isfinite(trump_min_series)

trump_series = np.array(graph_data['trump_unemployment']).astype(np.double)
trumpmask = np.isfinite(trump_series)

trump_max_series = np.array(graph_data['trump_max']).astype(np.double)
trumpmaxmask = np.isfinite(trump_max_series)


#Set up plot
hover = HoverTool(names=["foo"], 
                  tooltips = [("Date", "@Date_String"),  
                              ("Trump Unemployment", "@y%"),
                              ("Quote", "@Trump_Quote"),
                              #("Source", "@Trump_Location"),
                              ("Federal Unemployment", "@Federal_Unemployment%"),
                              #("Trump Location", "@Trump_Location"),
                              #("Series", "@Series_Name"),
                             ],
                 mode = 'mouse')

p = figure(tools=[#hover, 
			'pan', 'save', 'reset', 'wheel_zoom'], 
			x_axis_type="datetime",
			width=900, height=500, 
			toolbar_location="above")
			#title="Unemployment Rate",
			#resize, tap
p.yaxis.axis_label = "U.S. Unemployment Rate (%)"
p.xaxis.axis_label = "Date"


# Plot vertical lines:
election_time = datetime.strptime('Nov 8 2016', '%b %d %Y')
inauguration_time = datetime.strptime('Jan 20 2017  12:00PM', '%b %d %Y %I:%M%p')
p.line(x=[election_time,election_time], y=[0,52], color = "black",
       line_width = 2, line_dash='dashed')
p.line(x=[inauguration_time,inauguration_time], y=[0,52], color = "black",
       line_width = 2, line_dash='dashed')
election_label = Label(x=election_time.timestamp()*1000, y=15, x_offset=-6, text="Election", 
                       text_baseline="bottom", angle = 3.14159/2)
p.add_layout(election_label)
inauguration_label = Label(x=inauguration_time.timestamp()*1000, y=10, x_offset=-6, text="Inauguration", 
                           text_baseline="bottom", angle = 3.14159/2)
p.add_layout(inauguration_label)


# Plot lines and patch
p.line(x=time_series[trumpmask], y=trump_series[trumpmask], color = "firebrick",
          line_width = 4, name = "bar", legend = "Trump Unemployment Rate")

p.line(x=time_series[fedmask], y=fed_series[fedmask], color = "navy",
       line_width = 4, name = "bar", legend = "Federal Unemployment Rate")

p.patch(x=np.append(time_series[trumpmaxmask],time_series[trumpminmask][::-1]), 
        y=np.append(trump_max_series[trumpmaxmask],trump_min_series[trumpminmask][::-1]),
          color="firebrick", alpha=0.1, line_width=2)
p.legend.location = "top_left"



# Data for hover plot
source = ColumnDataSource({'x': time_series[trumpmask], 
                           'y':trump_series[trumpmask], 
                           'Date_String':graph_data['date_string'][trumpmask],
                           'Federal_Unemployment':graph_data['fed_rate'][trumpmask],
                           #'Trump_Location':graph_data['trump_location'][trumpmask],
                           'Trump_Quote':graph_data['trump_quote'][trumpmask]})

#Visual scatter points for hover
p.scatter('x', 'y', color="firebrick", size = 10, fill_color='white', line_width=2,
          legend = "Trump Unemployment Rate", name = "foo", source=source, 
          line_color="firebrick", hover_color='firebrick', hover_alpha=1.0)

#Extended radius points for hover
#p.scatter('x', 'y', color="firebrick", size = 30, alpha=0, line_alpha=0, 
#			name = "foo", source=source)



#Set up text
trump_text = Paragraph(width = 1000)
#print(source.data['Trump_Quote'])
#trump_text.text = source.data[
trump_text.text = "hello hello"


code = """
console.log(cb_data);
console.log(cb_obj);
//window.alert(2+4);
//console.log(5+6);
var data = cb_data.data;
//window.alert(data);
var new_text = cb_data.index['1d'];
trump_text.text = "Trump Statement: " + new_text;
trump_text.trigger('change');
"""

callback1 = CustomJS(args=dict(source=source, trump_text=trump_text), code=code)
p.add_tools(HoverTool(tooltips=None, callback=callback1))








# HOVER CALLBACK GOES HERE!!!
def callback(attr, old, new):
	print("hello!!!!!!")

#hover.js_on_change('value', callback)
p.on_change("value", callback)

#hover.on_change("value", callback)
#print(hover)



curdoc().title = "Trump Unemployment Index"
curdoc().add_root(column(p, trump_text))
