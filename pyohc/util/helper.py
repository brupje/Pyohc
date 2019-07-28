from datetime import datetime, timedelta

class axis:
  
  def __init__(self, labels, positions):
    self.labels = labels
    self.positions = positions
    
class axis_info:
  
  
  
  def __init__(self):
    
    self.day_by_quarter = self.get_day_by_quarters()
    self.day_by_hour = self.get_day_by_hours()
    self.month_by_day = self.get_month_by_day()
    self.past48_per_hour = self.get_past48_per_hour()
    

    
  def get_day_by_quarters(self):
    
    labels=[]
    positions=[]
    
    for h in range(0,25):
      labels.append('%02d' % (h) + ":" + '%02d' % (0))
      positions.append('%02d' % (h) + '0000' )
      for m in [15,30,45]:
        labels.append("")
        positions.append('%02d' % (h) + '%02d' % (m) + '00' )
        
    return axis(labels,positions)
    
  def get_day_by_hours(self):
    
    labels=[]
    positions=[]
    
    for h in range(0,25):
      labels.append('%02d' % (h) + ":" + '%02d' % (0))
      positions.append('%02d' % (h) + '0000' )

        
    return axis(labels,positions)
    
  def get_month_by_day(self):
    labels=[]
    positions=[]
   
    retval=[]
    for d in range(-29,1):
      positions.append( (datetime.today() - timedelta(days=-d)).strftime("%Y%m%d"))
      labels.append( (datetime.today() - timedelta(days=-d)).strftime("%d-%m"))
    return axis(labels,positions)
    
  def get_past48_per_hour(self):
    labels=[]
    positions=[]
   
    retval=[]
    for h in range(-47,0):
      positions.append( (datetime.today() - timedelta(hours=-h)).strftime("%Y%m%d_%H") + ('%02d' % (0)) + "00")
      labels.append(  (datetime.today() - timedelta(hours=-h)).strftime("%H-") +  "00")
      
    return axis(labels,positions)
  
 
