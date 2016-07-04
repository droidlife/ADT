from datetime import datetime
f = open('.atd_imp', 'r')
lines = f.readlines()
f.close()
f = open('.atd_imp', 'w')
for line in lines:
    if line.strip().__contains__('one piece'):
        f.write(line.replace('one piece', 'one') + '\n')
    else:
        f.write(line + '\n')

var = '22 june 2016'
date_object = datetime.strptime(var, '%d %B %Y')

date = datetime.now()
print date_object-date