from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model, schemas, errors
from sqlalchemy.orm import Session
from .database import engine, get_db

model.Base.metadata.create_all(bind=engine)

app = FastAPI()



''' 
##################################
CRUD OPERATIONS FOR POSTS MODULE
##################################
'''

# GET ALL POSTS 

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return posts

# GET A SINGLE POST BY AN ID

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post_id(id: int, db: Session=Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    errors.post_not_found(post, id) # Check if post is not found and raise HTTPException 
    return post

# CREATE A POST 

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db)):

    new_post = model.Post(**post.dict()) # **kwargs used.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# DELETE A POST 

@app.delete("/posts/{id}")
def delete_post(id: int, db: Session=Depends(get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    errors.post_not_found(post, id) # Check if post is not found and raise HTTPException 
    post.delete(synchronize_session=False) 
    #db.delete(post)  NOT WORKED
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE A POST 

@app.put("/posts/{id}", response_model=schemas.Post)
def update_posts(id: int,update_posts: schemas.PostCreate, db: Session=Depends(get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    errors.post_not_found(post, id) # Check if post is not found and raise HTTPException 
    post_query.update(update_posts.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()

''' 
##################################
CRUD OPERATIONS FOR USERS MODULE
##################################
'''

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)

def create_user(user: schemas.UsersCreate, db: Session=Depends(get_db)):

    new_user = model.User(**user.dict()) # **kwargs used.
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
  
