import re 
# from main_lib import *   
from fastapi import Depends, FastAPI , HTTPException ,File, UploadFile
from fastapi.param_functions import Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime, timedelta
from typing import Optional 
# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import numpy as np  
import base64
import requests
from lib.base64_handler import decode_b64_to_file
from lib.storage import Storage

from docxtpl import DocxTemplate
from docx2pdf import convert

   


class Urltob64(BaseModel): 
    url : str 

class Example(BaseModel): 
    foldername : str 
    productImage : str = Body(...,example="https://... ") 

class uploadFiles(BaseModel):
    Number : str
    Department : str
    Date : str
    Name : str

SECRET_KEY = "21bb28cfdac986bd041470db0ef8cbe32ecf18cfcea96163c6fc37f5ec6e4f89"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  

users_db = {
    "bst-service": {
        "username": "bst-service",
        "full_name": "thebrainstem",
        "email": "service@thebrainstem.com", 
        "hashed_password": "$2b$12$vIMfE/1F7l9PaKvncCkhmORVBygomq/iXJRHFspFkS8eA0hAmI54q",
        "disabled": False,
    }
}

app = FastAPI() 

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/")
def home(): 
    return {"message":" GET HOME "} 

@app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
def read_item_test(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
 
@app.post("/url-to-b64")
async def urltob64(reqest : Urltob64):  
    res = get_as_base64(url=reqest.url)
    return{ 
            'base64': res,   
        }  

@app.post("/example")
async def product_search_api(reqest : Example):  
    try: 
        foldername          =  reqest.foldername
        productImage        =  reqest.productImage 
        return{ 
            'foldername': foldername,  
            'productImage':  productImage  
        }  
    except ValueError as e:                                
        return{ 
            'error_code':  str(e),  
        } 
def DocxToStorage(FileDocxFromTemp,reqest):
    NameFile = FileDocxFromTemp
    doc = DocxTemplate(FileDocxFromTemp)
    context = { "Number" : reqest.Number , 
                "Department" : reqest.Department , 
                "Date" : reqest.Date , 
                "Name" : reqest.Name }
    doc.render(context)
    Segments = NameFile.rpartition('.')
    keyword = Segments[-3]
    file_name = f"{keyword}.docx"
    doc.save(file_name)                                                                                                                                                                                                                                                                                                                    
    return file_name 

def DocxToPdf(FileDocx,reqest):
    inputFile = FileDocx
    Segments = inputFile.rpartition('.')
    keyword = Segments[-3]
    outputFile = f"{keyword}.pdf"
    pdfFile = convert(inputFile, outputFile)
    with open(f'{reqest.filename}', "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())
    return encoded_string

@app.post("/pdf")
async def pdftob64( reqest : uploadFiles):
    NameFile = "app/template_N8.docx"
    FileDocx =  DocxToStorage(FileDocxFromTemp = NameFile,reqest = reqest)                                                                                                                                                                                                                                                                                                                   
    pdf = DocxToPdf(FileDocx=FileDocx,reqest=reqest)
     
    base64   = pdf 
    extension   = "pdf"
    folder   = "N_8" 
    try:  
        file_name = decode_b64_to_file(b64=base64, extension=extension)  
        ST = Storage(bucket_name = 'chaladohn_image_upload')
        result = ST.upload_to_bucket(blob_name=file_name,folder=folder)
        return result
    except ValueError as e:
        return{
            'error_code':  str(e),
        }
def get_as_base64(url): 
    return base64.b64encode(requests.get(url).content)

def test():
    print("test")
 

if __name__ == '__main__':
    endpoint = "https://i.stack.imgur.com/N4TSy.jpg"
    res = get_as_base64(url=endpoint)

    print(res)
