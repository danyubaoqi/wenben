import requests
a=requests.get("http://localhost:8014/?types=0").text
print(a)
