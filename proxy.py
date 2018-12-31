import requests
import json
class Proxy:
    def get_proxy(self):

        a=requests.get("http://54.245.156.160:8000/").text
        data=json.loads(a)
        return data
if __name__ == '__main__':
    a=Proxy()
    print(a.get_proxy())