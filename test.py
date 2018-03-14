from datetime import datetime
import time
a1 =  datetime(2017,1,1);
a2 = a1.strftime("%y-%m-%d")
string1 ="09/01/1991"
a3 = datetime.strptime("09/01/2017","%m/%d/%Y").strftime("%m/%d/%Y")
print a3
