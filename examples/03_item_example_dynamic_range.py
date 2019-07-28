# this example will generate a graph for the past 48 hours for a Temperature item like the previous example, with smoother
# lines and when the temperatures goes out of range of the Y-scale, the scale is adjusted

#import required and recommended modules
import pygal    
import mysql.connector

from pygal.style import DefaultStyle

import time
import numpy
import math
import pyohc.openhab
from pyohc.util.enums import *
from pyohc.util.helper import *

#globally define some variables
item = 'item_name' #replace this with one of the items in your setup
Chart_width = 800
Chart_height = 400
timezone = "Europe/Amsterdam"

#create mysql object
mydb = mysql.connector.connect(
  host="localhost",
  user="openhab",
  passwd="openhab",
  database="openhab"
)

#create openhab DB object
openhabdb = pyohc.openhab.data.db(mydb,timezone)

#create helper object for generating time axes
axis_info = pyohc.util.helper.axis_info();

#get dictionary with OpenHab items to item id (table) mapping
items = openhabdb.get_items()



#create a line chart object and set labels for x axis
chart = pygal.Line(title=u'Example Temperature (48 hours)', interpolate='cubic', legend_at_bottom=True, show_legend=True,x_label_rotation=45,width=Chart_width ,height=Chart_height, style=DefaultStyle, y_title='Temperature (°C)')
chart.x_labels = axis_info.past48_per_hour.labels

#retrieve the openhabd data
result = openhabdb.get_data(items[item],TimeMode.PAST_48HOURS, GroupMode.HOUR_WITH_DATE, AggMode.AVG, False)

#convert the data into series
serie = openhabdb.get_data_to_series(result,axis_info.past48_per_hour.positions)

# Default the range is between 15 and 25 degrees. But the scale will be adjusted when it goes out of range
chart.y_labels = range(math.floor(min(numpy.min(serie),15)),math.ceil(max(numpy.max(serie),25)))

#add chart series
chart.add('Temperature sensor', serie)
chart.render_to_png('/etc/openhab2/html/test.png')
