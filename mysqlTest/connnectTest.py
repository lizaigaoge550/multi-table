import pymysql
import glob

db = pymysql.connect('localhost','root','123456789','geo')

cursor = db.cursor()

fw = open('len_more_than_1.txt','w')
for eachfile in glob.glob('geosql\\*'):
    for line in open(eachfile,encoding='utf-8').readlines():
        line = line.strip()
        try:
            cursor.execute(line)
        except:
            print(eachfile)
            print(line)
        results = cursor.fetchall()
        if len(results) > 1:
            fw.write("file:{0}, sql:{1}".format(eachfile,line)+'\n')
fw.close()
