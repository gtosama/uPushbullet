from pushbullet import Pushbullet
import json

Key = '' #your api key

push = Pushbullet(Key)

print(push.api_key)
print(push.get_user_id())

phone_id = push.get_device_id('HUAWEI HUAWEI VNS-L31')#the phone id
print(phone_id)
data = {'type' : 'note' ,
        'body' : 'Hello from Micropython',
        'title': 'Alarm 1',
        'device_iden':phone_id} #standard push note

push.make_push(phone_id , json.dumps(data)) # send sms through your phone device
