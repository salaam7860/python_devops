from fastapi import FastAPI
from . import model
from .database import engine
from .routers import post, user, auth, votes
from .config import settings



# model.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


'''
select posts.*, users.email from posts left join users on posts.owner_id = users.id;

select * from posts right join users on posts.owner_id = users.id;

select users.id, users.email, count(posts.id) as user_post_count from posts right join users on posts.owner_id = users.id group by users.id;

select posts.*, count(votes.post_id) from posts left join votes on posts.id = votes.post_id group by posts.id;
'''


# https://youtu.be/0sOvCWFmrtA?t=39119