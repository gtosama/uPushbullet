import ujson
import urequests

class Pushbullet:
    url_dev  ='https://api.pushbullet.com/v2/devices'
    url = 'https://api.pushbullet.com/v2/pushes'
    
    def __init__(self , api_key):
        self.api_key = api_key
    
    def get_user_id(self):
        r = urequests.get('https://api.pushbullet.com/v2/users/me' ,headers={'Access-Token':self.api_key})
        res = ujson.loads(r.text)
        self.user_id = res['iden']
        return self.user_id
    
    def get_device_id(self , dev_name):
        r = urequests.get('https://api.pushbullet.com/v2/devices' , headers={'Access-Token':self.api_key,'Content-Type':'application/json'})
        res = ujson.loads(r.text)
        
        for d in res['devices'] :
            if(d['nickname'] == dev_name) :
                return d['iden']
        return None
    
    def make_push(self ,dev_id,JData) :
        urequests.post('https://api.pushbullet.com/v2/pushes' ,
                       headers={'Access-Token':self.api_key,'Content-Type':'application/json'}
                       ,data=JData)
    def send_sms(self,phone_num,phone_id,message):
        sms = {
              "push": {
                "conversation_iden": phone_num,
                "message": message,
                "package_name": "com.pushbullet.android",
                "source_user_iden": self.user_id,
                "target_device_iden": phone_id,
                "type": "messaging_extension_reply"
                  },
              "type": "push"
        }
        JData = ujson.dumps(sms)
        urequests.post('https://api.pushbullet.com/v2/ephemerals' ,
                       headers={'Access-Token':self.api_key,'Content-Type':'application/json'}
                       ,data=JData)