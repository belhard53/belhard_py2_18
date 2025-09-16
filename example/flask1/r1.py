import requests

res = requests.get('https://randomfox.ca/floof/')

d = res.json()

print(type(d), d)