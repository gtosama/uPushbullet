
#connect to wifi
from pushbullet import Pushbullet



# Example usage:
pb = Pushbullet('o.Bm0JqU1VlYjHNT4Cn0V5KMTkhfl0hiVF')
# 
# # Get user ID
user_id = pb.get_user_id()
print(f"User ID: {user_id}")
# 
# # Find device
device_id = pb.get_device_id('Google Pixel 4a')
if device_id:
#     # Send push
      pb.make_push(device_id, 'Test', 'Hello from MicroPython!')
#     
#     # Send SMS
#     pb.send_sms('+1234567890', device_id, 'Test SMS')
# 
# # List all devices
# devices = pb.list_devices()
# for dev in devices:
#     print(f"{dev['nickname']}: {dev['iden']}")