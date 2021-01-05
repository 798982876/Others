
import requests
import json
import time
import datetime 
from pandas import DataFrame
import psycopg2

#请求高德实时路况数据
def getGaodeTrafficStatus(key,rectangle,currentTime):
    insert_list = []
    TrafficStatusUrl = 'https://restapi.amap.com/v3/traffic/status/rectangle?key='+key+'&rectangle='+rectangle+'&extensions=all&level=6'
    requests.adapters.DEFAULT_RETRIES = 5
    res = requests.get(url=TrafficStatusUrl).content
    total_json = json.loads(res)
    try:
        jsondata = total_json['trafficinfo']['roads']
    except:
        return
    currentDate = time.strftime("%Y-%m-%d", time.localtime())
    if any(jsondata):
        for i in jsondata:
            name = i['name']
            status = i['status']
            direction = i['direction']
            angle = i['angle']
            speed = i.get('speed')
            # 若速度参数缺失，补为Null
            if speed == None:
                speed = None
            lcodes = i['lcodes']
            polyline = i['polyline']
            list = [name, status, direction, angle, lcodes, polyline, currentDate, currentTime, speed]
            insert_list.append(list)
        conn = psycopg2.connect(database="jtkk", user="jtkk", password="726322", host="132.1.11.157", port="5432")
        cur = conn.cursor()
        for i in insert_list:
            if len(i):
                cur.execute(
                    "insert into traffic.gaode_date_nanjing(name, status, direction, angle, lcodes, polyline, date, time,speed)  values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    i)
            conn.commit()
        conn.close()
    else:
        pass
    return



#建立覆盖研究区的rectangle数组
minx=118.5
miny=31.8
maxx=119.1
maxy=32.2 

x=minx
y=miny
rectangle=''
rectangleList=[]

while(y<=maxy):
    while(x<=maxx):
        rectangle=str(x)+','+str(y)+';'+str(x+0.06)+','+str(y+0.06)
        rectangleList.append(rectangle)
        rectangle=''
        x=x+0.06
    y=y+0.06
    x=minx
# rectangleList=['112.83037,22.774548;113.288003,23.324705','112.83037,22.774548;113.288003,23.324705','112.83037,22.774548;113.288003,23.324705',]





key='159a259fd4060da7b3a516dbb4335211'
#注册多个高德key,轮流使用，并记录请求的个数，满2000次换下一个key继续请求。
keyList=['db1e3d6ab3d95bf4f2271f0742f71442','e54bf9844d36fec9c411c9f481881ba6','b4aefc9121829bdd3255b096418ff5c1','265f25919184276960e967159ee948f5','562abb1a7114e29d2d04f4f01fb3893f','d20c01352544b797d45062b30b19d563']
keytimes=[0,0,0,0,0,0,0,0,0,0,0,0]
keyindex=0
dayindex=datetime.datetime.now().hour*12+datetime.datetime.now().minute/5

while True: 
    if datetime.datetime.now().minute % 5 == 0: 
        #创建请求时间，确保一次请求的时间都相同
        currentTime = time.strftime("%H:%M:%S", time.localtime())  # 设置请求时间
        for rectangle in rectangleList:
            if(keytimes[keyindex]>=30000):
                keyindex+=1
            key=keyList[keyindex]
            getGaodeTrafficStatus(key,rectangle,currentTime) 
            keytimes[keyindex]+=1
        print(time.localtime())
        time.sleep(60) 
        dayindex+=1
        if(dayindex>=288):
            dayindex=0
            keytimes=[0,0,0,0,0,0,0,0,0,0,0,0]
            keyindex=0
        
