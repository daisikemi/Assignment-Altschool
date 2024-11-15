from fastapi import FastAPI, HTTPException, Response, Form, Request
from pydantic import BaseModel, EmailStr, ValidationError, Field, field_validator
from typing import Optional, Annotated
from fastapi.middleware.cors import CORSMiddleware
import time
import logging


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    
                    handlers=[
                        logging.FileHandler("request.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger("main")


app = FastAPI()


origins = ["http://localhost:8000"]


app.add_middleware(
    CORSMiddleware, 
    allow_origins="http://127.0.0.1:8000", 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*'])

class User(BaseModel):
    username: str
    hashed_password: str
    firstname: str
    lastname: str
    age: int
    email: EmailStr
    height: str

   

class user(User):
    id: int



class usercreate(User):
    pass

    
users =[
    {"id":1,
    "username":"user1", 
    "hashed_password": "password1",
    "firstname": "Mary",
    "lastname":"Babalola",
    "age":"27",
    "email": "marybabs@gmail.com",
    "height":"172cm"},

    {"id":2, 
    "username":"user2",
    "hashed_password":"password2",
    "firstname":"Juliet", 
    "lastname":"Festus", "age":"24", 
    "email":"juliefestus@gmail.com", 
    "height":"168cm"}
]


@app.middleware("http")
async def log_request_time(request: "Request", call_next):
    start_time=time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Request to {request.url} took {duration:.5f} seconds")
    return response
    
    



  

@app.post("/create_user", status_code=201) #response_model=list[user] )
async def create_user(
    username:Annotated[str, Form],
    password: Annotated[str, Form],
    firstname:Annotated[str, Form],
    lastname:Annotated[str, Form],
    age:Annotated[int, Form],
    email:Annotated[str, Form],
    height:Annotated[str, Form],

):
    
    id = len(users) + 1
    new_user = user(
        id=id,
        username=username,
        hashed_password=password,
        firstname=firstname,
        lastname=lastname,
        age=age,
        email=email,
        height=height
)
    
    if new_user.email in users:
       raise HTTPException(status_code=409, detail="An account with this email already exist")
    
    users.append(new_user)
    return {"message": "Account created successfully", "data": new_user}

    


    
    
   