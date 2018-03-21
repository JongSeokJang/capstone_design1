import datetime
import os

now = datetime.datetime.now()
nowYear = now.strftime('%Y')
print(nowYear)

yearFile = nowYear + '.txt'

if os.path.exists(yearFile) :
    print("hihihi")
else:
    fp = open(yearFile, 'w+')
    fp.close()
