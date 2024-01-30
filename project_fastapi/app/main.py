from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model
from sqlalchemy.orm import Session
from .database import engine, get_db

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# create a class and make a template for the user and bound him/her. Use the pydantic lib "All this is for validation purpose".

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Check if post is not found and raise HTTPException 
def post_not_found(post, id):
       if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found") 
    

''' 
##############################
CRUD OPERATIONS
##############################
'''

# GET ALL POSTS 

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all
    return {"data" : posts}

# GET A SINGLE POST BY AN ID

@app.get("/posts/{id}")
def get_post_id(id: int, db: Session=Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    post_not_found(post, id) # Check if post is not found and raise HTTPException 
    return {"post_detail": post} 

# CREATE A POST 

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session=Depends(get_db)):

    new_post = model.Post(**post.dict()) # **kwargs used.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

# DELETE A POST 

@app.delete("/posts/{id}")
def delete_post(id: int, db: Session=Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id)
    if post.first() == None: # Check if post is not found and raise HTTPException 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} is deleted.")
    post.delete(synchronize_session=False) 
    #db.delete(post)  NOT WORKED
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

