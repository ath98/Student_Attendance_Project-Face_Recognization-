import datetime
from decimal import Decimal

t = "10:20"

hrs = t.split(':')[0]
min = t.split(':')[1]

time1 = hrs + '.' + min
print(time1)
print(Decimal(time1))

time = datetime.time(int(hrs),int(min))
print(str(time))


print("Time obj +"+ str(time.hour) + " " + str(time.minute))

print("Hrs : "+ hrs )
print("min : "+ min)

d = "2020-12-25"

year = d.split('-')[0]
month = d.split('-')[1]
day = d.split('-')[2]

print("year:"+year)
print("Month:"+month)
print("day:"+day)

roll = 51
shift = 1
year = 2

rollNumber = "5" + str(year) + str(shift) + str(roll)
print(rollNumber)