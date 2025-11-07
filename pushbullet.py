import ujson
import urequests
class PushbulletError(Exception):
    """Custom exception for Pushbullet API errors"""
    pass

class Pushbullet:
    """Pushbullet API client for MicroPython"""
    
    BASE_URL = 'https://api.pushbullet.com/v2'
    
    def __init__(self, api_key):
        """
        Initialize Pushbullet client
        
        Args:
            api_key: Your Pushbullet API access token
        """
        if not api_key:
            raise ValueError("API key cannot be empty")
        self.api_key = api_key
        self.user_id = None
    
    def _get_headers(self):
        """Get common headers for API requests"""
        return {
            'Access-Token': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, method, endpoint, data=None):
        """
        Make HTTP request with error handling
        
        Args:
            method: HTTP method ('GET' or 'POST')
            endpoint: API endpoint path
            data: Optional JSON data for POST requests
            
        Returns:
            Parsed JSON response
            
        Raises:
            PushbulletError: If request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"
        r = None
        
        try:
            if method == 'GET':
                r = urequests.get(url, headers=self._get_headers())
            elif method == 'POST':
                r = urequests.post(url, headers=self._get_headers(), data=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            if r.status_code not in (200, 201):
                raise PushbulletError(
                    f"API request failed with status {r.status_code}: {r.text}"
                )
            
            return ujson.loads(r.text)
            
        except Exception as e:
            raise PushbulletError(f"Request failed: {str(e)}")
        finally:
            if r:
                r.close()
    
    def get_user_id(self):
        """
        Fetch and cache user ID
        
        Returns:
            User ID string
        """
        if self.user_id:
            return self.user_id
            
        res = self._make_request('GET', 'users/me')
        self.user_id = res['iden']
        return self.user_id
    
    def get_device_id(self, dev_name):
        """
        Get device ID by device nickname
        
        Args:
            dev_name: Device nickname to search for
            
        Returns:
            Device ID string or None if not found
        """
        res = self._make_request('GET', 'devices')
        
        for device in res.get('devices', []):
            if device.get('nickname') == dev_name:
                return device['iden']
        
        return None
    
    def make_push(self, dev_id, title, body, push_type='note'):
        """
        Send a push notification
        
        Args:
            dev_id: Target device ID
            title: Push title
            body: Push body text
            push_type: Type of push (default: 'note')
        """
        push_data = {
            'device_iden': dev_id,
            'type': push_type,
            'title': title,
            'body': body
        }
        
        json_data = ujson.dumps(push_data)
        self._make_request('POST', 'pushes', data=json_data)
    
    def send_sms(self, phone_num, phone_id, message):
        """
        Send SMS via Pushbullet
        
        Args:
            phone_num: Target phone number/conversation ID
            phone_id: Source device ID (your Android device)
            message: SMS message text
        """
        # Ensure user_id is available
        if not self.user_id:
            self.get_user_id()
        
        sms_data = {
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
        
        json_data = ujson.dumps(sms_data)
        self._make_request('POST', 'ephemerals', data=json_data)
    
    def list_devices(self):
        """
        List all devices
        
        Returns:
            List of device dictionaries
        """
        res = self._make_request('GET', 'devices')
        return res.get('devices', [])

