import requests


res = requests.get("http://127.0.0.1:8000/users", params={'q':'123', 'f':'777'})
print(res.text)



for i in range(100):
     p = {'name':f"user_{i}", 'age':33}
     res = requests.post("http://127.0.0.1:8000/users", params=p)
     print(res.text)