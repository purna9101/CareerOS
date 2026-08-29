from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal 
from app.database import engine
from app.models import Base
from app.schemas import ApplicationCreate, ApplicationResponse
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


@app.get("/applications", response_model=list[ApplicationResponse])
def get_applications(db: Session  = Depends(get_db)):
    applications = db.query(Application).all()
    return applications 

@app.get("/applications/{application_id}" , response_model=ApplicationResponse)
def get_application(application_id : int, db: Session = Depends(get_db)):
    application = db.get(Application,application_id)
    if application is None:
        raise HTTPException(
            status_code = 404,
            detail=" application not found "
            )
    return application

@app.put("/applications/{application_id}", response_model=ApplicationCreate)
def update_application(application_id :int , data: ApplicationCreate,db:Session=Depends(get_db)):
    application =  db.get(Application,application_id)
    if application is None :
        raise HTTPException(
            status_code =404, 
            detail="application not found"
        )
    application.company = data.company
    application.position = data.position
    application.status = data.status

    db.commit()
    db.refresh(application)

    return application