# EXERCISE: add a Select widget to this example that offers several different greetings
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models.widgets import TextInput, Button, Paragraph, Select

# create some widgets
words = ["Hello", "Howdy", "Hola", "Sawubona"]

button = Button(label="Say HI")
select = Select(title="Word", value="Hello", options=words)
input = TextInput(value="Bokeh")
output = Paragraph()

# add a callback to a widget
def update():
    output.text = select.value + " " + input.value

button.on_click(update)

# create a layout for everything
layout = column(button, select, input, output)

# add the layout to curdoc
curdoc().add_root(layout)
