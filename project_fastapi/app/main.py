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



@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}
    