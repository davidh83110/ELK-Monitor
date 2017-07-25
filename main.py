"""
* Monitor ELK PRO 
*
* @author David
* Version 1.0 , 2017-07-25 , monitor health & disk
*
"""
#!/usr/bin/env python3

import requests
import os
import time
import json

# dingtalk
headers = {'Content-Type': 'application/json'}
r=requests.get('https://oapi.dingtalk.com/gettoken?corpid=ding92b8&corpsecret=7N6SwSq9',
headers=headers)
accessToken=json.loads(r.text)['access_token']

# health monitor
req_health = requests.get('http://22.15.24.15:9222/_cat/health')
health = req_health.text.split(' ')[3]

print(health)

if health == "red":
    print("critical")
    health_critical = os.popen('echo -e "ELK PRO Service CRITICAL.\nThe status is RED." | mail -s "`hostname` : ELK Status is RED" david_hsu@payeasy.com.tw')
    payload={
               "chatid":"chat68e0", # chatid is Alert Group in Dingtalk
               "msgtype": "text",
               "text": {
                   "content": "ELK PRO ALERT : Status is RED"
                   }
               }
    r = requests.post('https://oapi.dingtalk.com/chat/send?access_token={0}'.format(accessToken),data=json.dumps(payload),headers=headers) 
    f_health = open('/var/log/ELK_monitor.log','a')
    f_health.write("===========START===========\n")
    f_health.write("Time = "+time.strftime("%Y/%m/%d %H:%M:%S")+'\n')
    f_health.write("ELK PRO Status is RED\n")
    f_health.write("===========END===========\n")
    f_health.close()
else:
    print("ok")
    

# allocation monitor
req_allocation = requests.get('http://22.15.24.15:9222/_cat/allocation')
allocation = int(req_allocation.text.split(' ')[5])

print(allocation)

if allocation >= 70:
    print("disk critical")
    disk_critical = os.popen('echo -e "ELK PRO DISK CRITICAL.\nThe usage over 70%." | mail -s "`hostname` : ELK DISK over 70%" david_hsu@payeasy.com.tw')
    payload={
               "chatid":"chat6c7d0c71ae06", # chatid is Alert Group in Dingtalk
               "msgtype": "text",
               "text": {
                   "content": "ELK PRO ALERT : DISK usage over 70%"
                   }
               }
    r = requests.post('https://oapi.dingtalk.com/chat/send?access_token={0}'.format(accessToken),data=json.dumps(payload),headers=headers) 
    f_disk = open('/var/log/ELK_monitor.log','a')
    f_disk.write("===========START===========\n")
    f_disk.write("Time = "+time.strftime("%Y/%m/%d %H:%M:%S")+'\n')
    f_disk.write("ELK PRO DISK over 70%\n")
    f_disk.write("===========END===========\n")
else:
    print("disk ok")
