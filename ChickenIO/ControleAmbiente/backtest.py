import requests

#url = 'https://www.w3schools.com/python/demopage.php'
url = 'http://192.168.0.119:3000/environmental-log/store'
myobj = {'gabriel': 'cara'}

#x = requests.post(url, data = myobj)
x = requests.post(url, data = myobj)

print(x.text)