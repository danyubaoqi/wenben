import requests
import json
class Proxy:
    def get_proxy(self):

        a=requests.get("http://54.190.145.159:8000/").text
        data=json.loads(a)
        return data
if __name__ == '__main__':
    a=Proxy()
    print(a.get_proxy())