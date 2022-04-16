import re

ts = "#1-2-3,,,,,"
ts2 = "1,2,3,4,3,1"
tag = 'none'
if re.match(r'^#.+,,,,,', ts):
  tag = ts[1:-5]
print(tag)
if re.match(r'^([0-4],){5}\d$', ts2):
  tag = ''.join([x for x in ts2 if (x!=',')])
print(tag)