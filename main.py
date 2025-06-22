from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# Create a class fromt he pydantic model
class Post(BaseModel): 
    title: str 
    content: str 
    published: bool = True # bool = True means to set the bool value to True as defaule unless the user specify it (optional field)
    rating: Optional[int] = None # fully optional field, if none provided, the value will be null

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "Favorite foods", 
            "content": "I like pizza", "id":2}] # Where we save our posts

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/posts")
def get_posts(): # Retrieve all posts
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED) # add another parameter of status code to change the status code of a certain task 
def create_posts(new_post : Post): # by using pydantic model, it helps extracting the data directly without our own definition
    # try new_post.content, new_post.title, new_post.published, new_post.rating 
    # new_post.dict() --> convert the Post into a dictionary type    
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data" : post_dict} # return will appear in the api interface (or in this case Postman window)
# Title str, Content str, 

@app.get("/posts/{id}")
def get_post(id : int): # Retrieve singular post
 
    post = find_post(id)
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id {id} was not found"}
    return{"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) # status code 204 is used for deleting content
def delete_post(id : int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) # when deleting posts, return a response 204

@app.put("/posts/{id}")
def update_post(id: int, post: Post): # use the same pydantic model to keep the value of variable consistent with schema
    
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}