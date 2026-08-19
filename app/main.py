from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal 
from app.database import engine
from app.models import Base
from app.schemas import ApplicationCreate
from app.models import Application

app = FastAPI(
    title="CareerOS API",
    description="Backend API for managing and tracking job applications.",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)


@app.get("/", tags=["System"])
def home():
    return {
        "service": "CareerOS API",
        "status": "running",
        "version": "0.1.0",
    }

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@app.post("/applications")
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    new_application = Application(
        company=application.company,
        position=application.position,
        status=application.status,
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CareerOS API",
        "version": "0.1.0"
    }


