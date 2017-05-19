# To run from command line: bokeh serve --show tui.py

import pandas as pd
import numpy as np
from datetime import datetime
#from datetime import datetime as dt
from bokeh.layouts import column#, row, widgetbox
from bokeh.models import HoverTool, Legend
from bokeh.models import ColumnDataSource, Circle, OpenURL, TapTool
from bokeh.models.annotations import Span, Label
from bokeh.models.widgets import TextInput, Button, Paragraph, Select
from bokeh.plotting import figure, show
from bokeh.io import show, curdoc, vform


df = pd.read_csv("data.csv")
df['date_formatted']=df['date'].astype('datetime64[ns]')
df.dtypes

trump_text = Paragraph(width = 1000)
trump_text.text = "Hello world"


# Import Data
start_date = '2015-06-01'
graph_data = df.loc[df['date_formatted'] >= start_date]
graph_data.index = pd.DatetimeIndex(graph_data['date'])
graph_data['date_string'] = graph_data['date'].astype(str)
graph_data['trump_unemployment'] = graph_data['trump_unemployment'].round()


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


p = figure(tools=[#hover, 
	'tap', 'pan', 'save', 'reset', 'wheel_zoom'], 
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
inauguration_label = Label(x=inauguration_time.timestamp()*1000, y=10, x_offset=-6, text="Inauguration", text_baseline="bottom", angle = 3.14159/2)
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


"""
# Plot scatter plot with hover:
renderer = p.circle(time_series[trumpmask], trump_series[trumpmask], color="firebrick",
        size = 10, fill_color='white', legend = "Trump Unemployment Rate")

selected_circle = Circle(fill_color="firebrick")
nonselected_circle = Circle(fill_color="white", line_color="firebrick", size = 10)

renderer.selection_glyph = selected_circle
renderer.nonselection_glyph = nonselected_circle
"""

# Highlight particular points

renderer = p.circle(time_series[trumpmask], trump_series[trumpmask], #color="firebrick",
				legend = "Trump Unemployment Rate", size=12,
				fill_color="white", fill_alpha=1.0, line_color="firebrick", line_alpha=1.0,

						# set visual properties for selected glyphs
						selection_color="firebrick",

						# set visual properties for non-selected glyphs
						nonselection_fill_color="white",
						nonselection_fill_alpha=1.0,
						nonselection_line_color="firebrick",
						nonselection_line_alpha=1.0)


name_for_display = np.tile('trump_unemployment', [len(time_series[trumpmask]),1])
print(name_for_display)

def update_text(attrname, old, new):
	print("hello world")
	print(attrname)
	print(old)

#renderer.on_change('value', update_text)

#url = "http://www.colors.commutercreative.com/@color/"
#taptool = p.select(type=TapTool)
#taptool.callback = OpenURL(url=url)
#taptool.callback = update_text("value")

print(selected_circle)
print("hello1")
print(renderer)
print("hello2")

curdoc().title = "Trump Unemployment Index"
curdoc().add_root(column(p, trump_text))


"""
from bokeh.models import ColumnDataSource, OpenURL, TapTool
from bokeh.plotting import figure, output_file, show

output_file("openurl.html")

p = figure(plot_width=400, plot_height=400,
           tools="tap", title="Click the Dots")

source = ColumnDataSource(data=dict(
    x=[1, 2, 3, 4, 5],
    y=[2, 5, 8, 2, 7],
    color=["navy", "orange", "olive", "firebrick", "gold"]
    ))

p.circle('x', 'y', color='color', size=20, source=source)

url = "http://www.colors.commutercreative.com/@color/"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)

show(p)
"""




