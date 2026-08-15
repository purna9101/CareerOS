from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal 
from app.database import engine
from app.models import Base
from app.schemas import ApplicationCreate
from app.models import Application

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "CareerOS Backend Running 🚀"}

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@app.get("/applications")
def Create_application(application: ApplicationCreate, db: Session = Depends(get_db):
    new_application = Application(company=application.company,
                                  position = application.position,
                                  status=application.status,
                                  )
                                  