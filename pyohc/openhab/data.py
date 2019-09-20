
from pyohc.util.enums import *
import mysql.connector
class db:
  
  def __init__(self, mysqlconn, timezone):
    self.mydb = mysqlconn
    self.timezone = timezone
    
  def get_items(self):
    cursor = self.mydb.cursor()
    cursor.execute("select ItemID,ItemName from Items")
    result = list(cursor.fetchall())
    retval = dict()
    for t in result:
      retval[t[1]] = "Item"+ str(t[0])


    return retval
    
    
  def get_data(self, view, timemode, groupmode, aggmode, num_records):
    
    if groupmode == GroupMode.MONTH_MAX_DAY:
      basequery = "\
        from (\
	        select date_format(CONVERT_TZ(Time,'+00:00', '"+self.timezone+"'), '%Y%m%d') timecol, max(Value )val \
	        FROM "+view+" \
	        group by timecol\
        ) q \
      "
    else:
      basequery = "\
        from (\
	        select CONVERT_TZ(Time,'+00:00', '"+self.timezone+"') timecol, Value val \
	        FROM "+view+" \
        ) q \
      "
      
    if timemode == TimeMode.PAST_48HOURS:
      basequery += "where timecol between DATE_SUB(current_time(), interval 48 hour) and current_time()\n"
    elif timemode == TimeMode.TODAY:
      basequery += "where date(timecol) = current_date()\n"
    elif timemode == TimeMode.YESTERDAY:
      basequery += "where date(timecol) = DATE_SUB(current_date(), interval 1 day)\n"
    elif timemode == TimeMode.PAST_30DAY:
      basequery += "where date(timecol) between DATE_SUB(current_date(), interval 30 day) and current_date()\n"
    elif timemode == TimeMode.PAST_30DAY_DAYTIME:
      basequery += "where date(timecol) between DATE_SUB(current_date(), interval 30 day) and current_date()\
        and time(timecol) BETWEEN '10:00:00' AND '16:00:00' \n"
        
      
      
    rowlimit=""
    if num_records:
      rowlimit += "limit " + str(num_records)  

    column = ""
    if aggmode == AggMode.MAX:
      column = "max(val)"
    elif aggmode == AggMode.AVG:
      column = "avg(val)"
    elif aggmode == AggMode.MIN:
      column = "min(val)"
    elif aggmode == AggMode.SUM:
      column = "sum(val)"
        
    if groupmode == GroupMode.QUARTER_HOUR:
      group_expr = "date_format(FROM_UNIXTIME(FLOOR(UNIX_TIMESTAMP(timecol)/(15 * 60))*(15 * 60)), '%H%i%s')"
    elif groupmode == GroupMode.HOUR:
      group_expr = "date_format(timecol, '%H0000')"
    elif groupmode == GroupMode.HOUR_WITH_DATE:
      group_expr = "date_format(timecol, '%Y%m%d_%H0000')"
    elif groupmode == GroupMode.DAY:
      group_expr = "date_format(timecol, '%Y%m%d')"
    elif groupmode == GroupMode.MONTH or groupmode == GroupMode.MONTH_MAX_DAY:
      group_expr = "date_format(timecol, '%Y%m')"  
      
        
    basequery = "select round(val,1) colval,lab \
      from (\
       select "+group_expr+" lab, " + column + " val " + basequery + "\
       group by lab\
       order by timecol desc\
       " + rowlimit + "\
       )q2 \
       order by lab"; 
    cursor = self.mydb.cursor()
    try:
      cursor.execute( basequery )   
      print(basequery)

      return list(cursor.fetchall()) 
    except mysql.connector.Error as err:
      raise Exception("Error executing query\n{}\n{}".format(basequery,err));
  def get_data_to_series(self,result,labels):
    retval = []
    tempdict = dict();
    for t in result:
      tempdict[str(t[1])] = (float(t[0]))

    for i in labels:
      if i in tempdict:
        retval.append(tempdict[i])  
      else:
        retval.append(0)  
        
    return retval
   
  def get_series_data(self, view, timemode, groupmode, aggmode, num_records, labels):
    result = self.get_data(view, timemode, groupmode, aggmode, num_records)
   
    return self.get_data_to_series(result,labels)
    
  def get_labels_from_data(self, data):
    retval = []
    for t in data:
      retval.append(t[1])  
    return retval
