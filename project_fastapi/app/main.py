from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model, schemas, errors, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, user, auth


model.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNH0.0AZDlVQnncYoa91yVzI0_cmLVh4pZ76VpY9vi-zjlrQ
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNCwiZXhwIjoxNzA3MTM2MTMwfQ.c8Kx6usyk6g60aqrX5pjiAHodrW7no-ev9Y931c1e8w

# https://youtu.be/0sOvCWFmrtA?t=29220