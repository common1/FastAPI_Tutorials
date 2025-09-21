from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)

BOOKS = []

@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Books).all()

@app.post("/")
def create_book(book: Book, db: Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()
    db.refresh(book_model)

    return book_model

@app.put("/{book_id}")
def update_book(book_id: int, book: Book, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if not book_model:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exist"
        )
    
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()
    db.refresh(book_model)

    return book_model

@app.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if not book_model:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exist"
    )

    # db.delete(book_model)
    db.query(models.Books).filter(models.Books.id == book_id).delete()
    db.commit()

    return {"detail": f"ID {book_id} : Deleted"}

#002
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/{name}")
# def read_api(name: str):
#     return {"Welcome": name}

#001
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_api():
#     return {"Welcome": "Harrie Smulders"}


