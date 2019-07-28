# this example will generate a multi-serie graph for the past 48 hours for 4 items

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
item1 = 'item_name' #replace this with one of the items in your setup
item2 = 'item_name' #replace this with one of the items in your setup
item3 = 'item_name' #replace this with one of the items in your setup
item4 = 'item_name' #replace this with one of the items in your setup

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



#add chart series
chart.add('Temperature sensor 1', openhabdb.get_series_data(items[item1],TimeMode.PAST_48HOURS, GroupMode.HOUR_WITH_DATE, AggMode.AVG, False,axis_info.past48_per_hour.positions))
chart.add('Temperature sensor 2', openhabdb.get_series_data(items[item2],TimeMode.PAST_48HOURS, GroupMode.HOUR_WITH_DATE, AggMode.AVG, False,axis_info.past48_per_hour.positions))
chart.add('Temperature sensor 3', openhabdb.get_series_data(items[item3],TimeMode.PAST_48HOURS, GroupMode.HOUR_WITH_DATE, AggMode.AVG, False,axis_info.past48_per_hour.positions))
chart.add('Temperature sensor 4', openhabdb.get_series_data(items[item4],TimeMode.PAST_48HOURS, GroupMode.HOUR_WITH_DATE, AggMode.AVG, False,axis_info.past48_per_hour.positions))

chart.render_to_png('/etc/openhab2/html/test.png')
