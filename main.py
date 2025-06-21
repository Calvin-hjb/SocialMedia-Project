from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Create a class fromt he pydantic model
class Post(BaseModel): 
    title: str 
    content: str 
    published: bool = True # bool = True means to set the bool value to True as defaule unless the user specify it (optional field)
    rating: Optional[int] = None # fully optional field, if none provided, the value will be null


@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.post("/createposts")
def create_posts(new_post : Post): # by using pydantic model, it helps extracting the data directly without our own definition
    print(new_post.rating) # try new_post.content, new_post.title, new_post.published, new_post.rating 
    print(new_post.dict()) # convert the Post into a dictionary type    
    return {"data" : new_post} # return will appear in the api interface (or in this case Postman window)
# Title str, Content str, 