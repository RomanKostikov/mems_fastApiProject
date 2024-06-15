from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.main import get_db
from app.api.models import Meme
# сервис с публичным API с бизнес-логикой
router = APIRouter()


@router.get("/memes")
def get_memes(db: Session = Depends(get_db)):
    memes = db.query(Meme).all()
    return memes


@router.get('/memes/{id}', response_model=Meme)
def get_meme(id: int, db: Session = Depends(get_db)):
    meme = db.query(Meme).get(id)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return meme


@router.post('/memes', response_model=Meme)
def create_meme(meme: Meme, db: Session = Depends(get_db)):
    db.add(meme)
    db.commit()
    db.refresh(meme)
    return meme


@router.put('/memes/{id}', response_model=Meme)
def update_meme(id: int, meme: Meme, db: Session = Depends(get_db)):
    db_meme = db.query(Meme).get(id)
    if not db_meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    db_meme.image_url = meme.image_url
    db_meme.text = meme.text
    db.commit()
    db.refresh(db_meme)
    return db_meme


@router.delete('/memes/{id}')
def delete_meme(id: int, db: Session = Depends(get_db)):
    meme = db.query(Meme).get(id)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    db.delete(meme)
    db.commit()
