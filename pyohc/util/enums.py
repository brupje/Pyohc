from enum import Enum

class TimeMode(Enum):
  TODAY = 0
  YESTERDAY = 1
  PAST_48HOURS = 2
  PAST_20DAY = 3
  PAST_30DAY = 4
  PAST_30DAY_DAYTIME = 5
  FOREVER = 6
  
class GroupMode(Enum):
  QUARTER_HOUR = 0
  HOUR = 1
  HOUR_WITH_DATE = 2
  DAY = 3
  MONTH = 4
  MONTH_MAX_DAY = 5
  
  
class AggMode(Enum):
  MAX = 0
  AVG = 1
  SUM = 2
  MIN = 3
