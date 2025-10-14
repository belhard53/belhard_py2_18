# pip install uvicorn
# pip install fastapi

from fastapi import FastAPI, Depends
import uvicorn
from pydantic import BaseModel



app = FastAPI()

class User1(BaseModel):
    name: str
    age: int | None = None
    

@app.get('/', tags=['inDex get'])
def home():
    return {"hello1": "python", "hello2": 'fastapi'}

# /users/?f=123456'
@app.get('/users', tags=['usersGET'])
def users(f: str='123', q:str=None):
    return {"status": "success", "data": 'data1', 'f':f, 'q':q}


@app.post('/users', tags=['userPOST'])
def home_post(user: User1 = Depends()):
    # print(user)
    return {"status": "success post", "data": {'id':1, 'add_user':f'{user.name} {user.age}'}}




if __name__ == '__main__':    
    uvicorn.run("main1:app", reload=True)  

# uvicorn main1:app --reload  
# uvicorn main1:app --host 0.0.0.0 --port 8000 --reload  