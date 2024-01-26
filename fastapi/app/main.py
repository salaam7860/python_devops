from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
app = FastAPI()

# creatr a class and make a template for the user and bound him/her. Use the pydantic lib "All this is for validation purpose".



class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# request: Get method url: "/"

@app.get("/")
def root():
    return {"message": "Welcome to the fastapi World!!"}

# [{"title": "title of post 1", "content": "content of post 1", "id":1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]
my_post = [{"title": "title of post 1", "content": "content of post 1", "id":1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]


@app.get("/post")
def post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"message": posts}


@app.post("/post", status_code=status.HTTP_201_CREATED) # when someone create a post status code will be generated 
def create_post(post: Post):
    # post_dict = post.dict() # post_dict["id"] = randrange(1, 100000) # my_post.append(post_dict)
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                  (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    # To save the changes you have to commit 
    conn.commit()
    return {'data': new_post}

@app.get("/post/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,)) # id, is a tuple if it is a string there is a risk of sql-injection 
    post = cursor.fetchone()
    post_not_found(post, id)   # Check if post is not found and raise HTTPException
    return {"post_detail": post}   

# the below lines are the other way of or sloppy way of writing the code ######
#response.status_code = status.HTTP_404_NOT_FOUND
#return {"Message": f"Post with id {id} was not found"}
        
# Check if post is not found and raise HTTPException 
def post_not_found(post, id):
       if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found") 

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p

# Now delete a request 

def find_index(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i


    

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,),)
    deieted_post = cursor.fetchone()
    conn.commit()
    post_not_found(deieted_post, id) # Check if post is not found and raise HTTPException

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# It updates an existing post within a list of posts, presumably stored as dictionaries within a list called my_post.

@app.put("/post/{id}", status_code=status.HTTP_200_OK)
def update_posts(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                  (post.title, post.content, post.published, id))
    posts = cursor.fetchone()
    conn.commit()
    post_not_found(posts, id)   # Check if post is not found and raise HTTPException
    return {"data": posts}

# Finding Index: 
    # index = find_index(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with requested id: {id} doesn't exist.")

# Creating Dictionary:
    # post_dict = post.dict()
# Updating ID: It explicitly sets the id key within the post_dict to the provided id value.
    # post_dict["id"] = id
# Assigning to List: it replaces the existing post at the found index in the my_post list with the updated post_dict.
    # my_post[index] = post_dict
    

'''
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
DATABASE CODING STARTS FROM HERE 
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
'''

while True:
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='123456', row_factory=dict_row)
        cursor = conn.cursor()
        print("Database is connected successfully!!")
        break
    except Exception as error:
        print("connecting to database failed")
        print("Error:", error)
        time.sleep(2)

# https://youtu.be/0sOvCWFmrtA?t=15117