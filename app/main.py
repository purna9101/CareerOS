from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal 
from app.database import engine
from app.models import Base
from app.schemas import ApplicationCreate, ApplicationResponse, ApplicationDelete, ApplicationUpdate 
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
def get_applications(
    company: str | None = None,
    position: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)):

    query = db.query(Application)
    if company is not None:
        company = company.strip()
        if company:
            query = query.filter(Application.company.ilike(f"%{company}%"))
    if position is not None:
        position = position.strip()
        if position:
            query = query.filter(Application.position.ilike(f"%{position}%"))
    if status is not None:
        status = status.strip()
        if status:
            query = query.filter(Application.status.ilike(status))

    applications = query.all()
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


@app.delete("/applications/{application_id}", response_model=ApplicationDelete)
def delete_application(application_id :int, db:Session=Depends(get_db)):
    application = db.get(Application,application_id)
    if application is None:
        raise HTTPException(
            status_code=404,
            detail="application not found"
        )
    db.delete(application)
    db.commit()
    return {"message":"application deleted"}


@app.patch("/applications/{application_id}",response_model=ApplicationCreate)
def patch_application(application_id :int, data : ApplicationUpdate, db :Session=Depends(get_db)):
    application = db.get(Application,application_id)
    if application is None:
        raise HTTPException(
            status_code=404,
            detail="application not found"
        )
    if data.company is not None:
        application.company = data.company
    if data.position is not None:
        application.position = data.position
    if data.status is not None:
        application.status = data.status
    db.commit()
    db.refresh(application)

    return application