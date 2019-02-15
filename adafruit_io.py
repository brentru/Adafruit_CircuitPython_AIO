"""
`adafruit_io.py`
================================================================================
Adafruit IO Client Wrapper.

Author(s): Brent Rubell for Adafruit Industries
"""

class Client(object):
    def __init__(self, username, key, wifi_manager, api_version='v2'):
        """
        Adafruit IO API REST Client
        :param str username: Adafruit IO Username
        :param str key: Adafruit IO Key
        :param wifi_manager: ESP32WiFiManager Object
        :param str api_version: Adafruit IO REST API Version
        """
        self.api_version = api_version
        self.url = 'https://io.adafruit.com/api/'+ self.api_version + '/'
        self.username = username
        self.key = key
        self.wifi = wifi_manager
        print('DEBUG: WIFI Manager: ', self.wifi)
        self.headers = {bytes("X-AIO-KEY","utf-8"):bytes(self.key,"utf-8")}

    # TODO: Add Method to construct paths

    # TODO: Add Error Handling

    # TODO: Add receive() method


    def send(self, data, feed):
        """
        Sends data to Adafruit IO on specified feed.
        :param data: Data to send to Adafruit IO
        :param feed: Specified Adafruit IO Feed
        """
        payload = {'value':data}
        path = self.url+self.username+"/feeds/"+feed+"/data"
        response = self.wifi.post(
            path,
            json=payload,
            headers=self.headers)
        #print(response.json())
        response.close()

    def receive(self, feed):
        """Return the most recent value for the specified feed.
        :param string feed: Name/Key/ID of Adafruit IO feed.
        """
        path = self.url+self.username+"/feeds/"+feed+"/data/last"
        response = self.wifi.get(
            path,
            headers=self.headers)
        return response.json()
        response.close()
