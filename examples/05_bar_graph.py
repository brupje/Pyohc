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


result = openhabdb.get_data(items[item],TimeMode.FOREVER, GroupMode.MONTH_MAX_DAY, AggMode.SUM ,False) 
labels = openhabdb.get_labels_from_data(result)

#create a line chart object and set labels for x axis
chart = pygal.Bar(title=u'Solar production per month',x_label_rotation=45,width=Chart_width ,height=Chart_height, interpolate='cubic', legend_at_bottom=True, show_legend=True, style=DefaultStyle, y_title='Production (KWh)')

chart.y_labels = 0, 500,1000,1500, 2000
chart.x_labels = labels
chart.add('Solar production', openhabdb.get_data_to_series(result,labels))
chart.render_to_png('/etc/openhab2/html/test.png')
