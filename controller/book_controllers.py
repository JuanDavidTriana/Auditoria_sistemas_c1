from fastapi import APIRouter, Depends, HTTPException, status
from model.shemas import BookCreate, BookOut
from repository.book_repository import BookRepository
from controller.deps import get_db, get_current_user, require_admin
from typing import Any

router = APIRouter(prefix="/books")

@router.get("/", response_model=list[BookOut])
async def list_books( q:str | None = None, limit: int = 20, skip: int = 0, db: Any = Depends(get_db)):
    repo = BookRepository(db)
    filter = {"$text": {"$search": q}} if q else {}
    return await repo.find(filter=filter, limit=limit, skip=skip)
    
@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: Any= Depends(get_db)):
    #await require_admin(user)
    repo = BookRepository(db)
    data = book.model_dump() # Convert Pydantic model to dict
    book_id = await repo.create(data)
    return {"id": book_id, **data}

@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: str, db: Any= Depends(get_db)):
    #await require_admin(user)
    repo = BookRepository(db)
    book = await repo.find_by_id(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
    return book
