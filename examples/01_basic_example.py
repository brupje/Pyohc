#this example will generate a graph for today, with 11 random numbers

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
chart = pygal.Line(title=u'Example',x_label_rotation=45,width=Chart_width ,height=Chart_height, style=DefaultStyle, y_title='Example values')
chart.x_labels = axis_info.day_by_hour.labels

#add chart series
chart.add('Data today', openhabdb.get_series_data('(\
  select RAND()*10 Value, current_timestamp()Time \
  union all \
  select RAND()*10 , date_sub(current_timestamp(), interval 1 hour)\
  union all \
  select RAND()*10 , date_sub(current_timestamp(), interval 2 hour)\
  union all \
  select RAND()*10 , date_sub(current_timestamp(), interval 3 hour)\
  union all \
  select RAND()*10 , date_sub(current_timestamp(), interval 4 hour)\
  union all \
  select RAND()*10 , date_sub(current_timestamp(), interval 5 hour)\
  union all \
  select RAND()*10 , date_sub(current_timestamp(), interval 6 hour)\
  union all \
  select RAND()*10 , date_sub(current_timestamp(), interval 7 hour)\
  union all \
  select RAND()*10 , date_sub(current_timestamp(), interval 8 hour)\
  union all \
  select RAND()*10 , date_sub(current_timestamp(), interval 9 hour)\
  union all \
  select RAND()*10 , date_sub(current_timestamp(), interval 10 hour)\
  ) data\
  ',TimeMode.TODAY, GroupMode.HOUR, AggMode.MAX ,False,axis_info.day_by_hour.positions))
chart.render_to_png('/etc/openhab2/html/test.png')
