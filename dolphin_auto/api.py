import requests


class DolphinRemoteApi:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.access_token = self.__get_access_token()
        self.cpu_list = [2, 4, 6, 8, 12, 16]
        self.memory_list = [2, 4, 8]

    def __get_access_token(self):
        url = 'https://anty-api.com/auth/login'

        data = {
            'username': self.username,
            'password': self.password
        }

        headers = {}

        r = requests.post(url, headers=headers, data=data).json()
        return r["token"]

    def get_profile_id_by_name(self, profile_name):
        url = 'https://anty-api.com/browser_profiles'

        params = {
            'query': profile_name
        }

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        r = requests.get(url, headers=headers, params=params).json()
        profile_id = r['data'][0]['id']
        return profile_id

    def get_useragent_fingerprint(self, browser_version=107):
        url = 'https://anty-api.com/fingerprints/useragent'

        params = {
            'browser_type': 'anty',
            'browser_version': browser_version,
            'platform': 'windows'
        }

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        r = requests.get(url, headers=headers, params=params).json()
        return r['data']

    def get_webgl_fingerprint(self, browser_version=107):
        url = 'https://anty-api.com/fingerprints/webgl'

        params = {
            'browser_type': 'anty',
            'browser_version': browser_version,
            'platform': 'windows',
            'type': 'webgl'
        }

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        r = requests.get(url, headers=headers, params=params).json()
        webgl_info = {'vendor': r['webgl_unmasked_vendor'], 'renderer': r['webgl_unmasked_renderer']}
        return webgl_info

    def get_new_fingerprints(self, screen='1536x864', browser_version=107):
        url = 'https://anty-api.com/fingerprints/fingerprint'

        params = {
            'browser_type': 'anty',
            'browser_version': browser_version,
            'screen': screen,
            'platform': 'windows',
            'type': 'fingerprint'
        }

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        r = requests.get(url, headers=headers, params=params).json()
        return r

    def create_browser_profile(self, profile_name, existing_proxy_id=None):
        url = 'https://anty-api.com/browser_profiles'

        fingerprints = self.get_new_fingerprints()
        useragent = fingerprints['userAgent']
        vendor = fingerprints['webgl']['unmaskedVendor']
        renderer = fingerprints['webgl']['unmaskedRenderer']
        webgl_max = fingerprints['webgl2Maximum']
        cpu = fingerprints['hardwareConcurrency']
        memory = fingerprints['deviceMemory']

        json_data = {
            'name': profile_name,
            'proxy': existing_proxy_id,
            'browserType': 'anty',
            "uaFullVersion": "107.0.5304.62",
            'tags': [],
            'args': [],
            'statusId': 0,
            'platform': 'windows',
            'mainWebsite': "",
            'doNotTrack': False,
            'webrtc': {
                'mode': 'altered',
                'ipAddress': None
            },
            'canvas': {
                'mode': 'noise'
            },
            'webgl': {
                'mode': 'noise'
            },
            'clientRect': {
                'mode': 'noise'
            },
            'notes': {
                'content': None,
                'color': 'blue',
                'style': 'text',
                'icon': 'info'
            },
            'useragent': {
                'mode': 'manual',
                'value': useragent
            },
            'webglInfo': {
                'mode': 'manual',
                'vendor': vendor,
                'renderer': renderer,
                'webgl2Maximum': webgl_max
            },
            'cpu': {
                'mode': 'manual',
                'value': cpu
            },
            'memory': {
                'mode': 'manual',
                'value': memory
            },
            'screen': {
                'mode': 'real',
                'resolution': None
            },
            'timezone': {
                'mode': 'auto',
                'value': None
            },
            'locale': {
                'mode': 'auto',
                'value': None
            },
            'geolocation': {
                'mode': 'auto',
                'latitude': None,
                'longitude': None,
                'accuracy': None
            },
            'audio': {
                'mode': 'real'
            },
            'mediaDevices': {
                'mode': 'real',
                'audioInputs': None,
                'videoInputs': None,
                'audioOutputs': None
            },
        }

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        r = requests.post(url, headers=headers, json=json_data).json()
        return r['browserProfileId']

    def delete_browser_profile(self, profile_id):
        url = 'https://anty-api.com/browser_profiles'

        json_data = {
            'ids': [profile_id]
        }

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        r = requests.delete(url, headers=headers, json=json_data)
        return r.text

    def import_cookies(self, profile_id, cookies):
        url = 'https://sync.anty-api.com/'

        params = {
            'actionType': 'importCookies',
            'browserProfileId': profile_id
        }

        json_data = {
            'cookies': cookies
        }

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        r = requests.post(url, headers=headers, params=params, json=json_data)
        return r.text


def start_browser_profile(profile_id):
    url = f'http://localhost:3001/v1.0/browser_profiles/{profile_id}/start'

    params = {
        'automation': 1
    }

    r = requests.get(url, params=params).json()
    print(r)
    return r['automation']['port'], r['automation']['wsEndpoint']


def close_browser_profile(profile_id):
    url = f'http://localhost:3001/v1.0/browser_profiles/{profile_id}/stop'

    r = requests.get(url)
    return r.text
