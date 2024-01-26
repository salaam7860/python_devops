from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
import psycopg
from psycopg.rows import dict_row
import time
app = FastAPI()

# create a class and make a template for the user and bound him/her. Use the pydantic lib "All this is for validation purpose".

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# request: Get method url: "/"

@app.get("/")
def root():
    return {"message": "Welcome to the fastapi World!!"}

@app.get("/post")
def post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"message": posts}

@app.post("/post", status_code=status.HTTP_201_CREATED) # when someone create a post status code will be generated 
def create_post(post: Post):
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

# Check if post is not found and raise HTTPException 
def post_not_found(post, id):
       if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found") 
    

'''
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
CONNECTING DATABBASE 
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

