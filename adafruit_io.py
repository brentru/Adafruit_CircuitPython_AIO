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
        self.url = 'https://io.adafruit.com/api'
        self.username = username
        self.key = key
        self.wifi = wifi_manager
        print('DEBUG: WIFI Manager: ', self.wifi)
        self.headers = {bytes("X-AIO-KEY","utf-8"):bytes(self.key,"utf-8")}

    # TODO: Add Error Handling

    def _compose_path(self, path):
      return "{0}/{1}/{2}/{3}".format(self.url, self.api_version, self.username, path)
    
    def _create_data(self, data, latitude, longitude, elevation, timestamp):
      return {'value':data, 'lat':latitude, 'lon':longitude,
                'ele':elevation, 'created_at':timestamp}

    def _post(self, path, packet):
        """
        Send data to Adafruit IO.
        :param str path: Composed URL
        :param json packet: JSON data to send to Adafruit IO
        """
        response = self.wifi.post(
            path,
            json = packet,
            headers = self.headers)
        response.close()

    def _get(self, path):
        response = self.wifi.get(
            path,
            headers=self.headers)
        return response.json()
        response.close()

    def send(self, feed, data, lat=None, lon=None, ele=None, created_at=None):
        """
        Sends value data to Adafruit IO on specified feed.
        :param data: Data to send to Adafruit IO
        :param feed: Specified Adafruit IO Feed
        :param int lat: Optional latitude
        :param int lon: Optional longitude
        :param int ele: Optional elevation
        :param string created_at: Optional date/time string
        """
        path = self._compose_path("feeds/{0}/data".format(feed))
        packet = self._create_data(data, lat, lon, ele, created_at)
        self._post(path, packet)

    def receive(self, feed):
        """Return the most recent value for the specified feed.
        :param string feed: Name/Key/ID of Adafruit IO feed.
        """
        path = self._compose_path("feeds/{0}/data/last".format(feed))
        return self._get(path)
        
