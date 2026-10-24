from sqlalchemy import CheckConstraint,Column, Integer, String
from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(255), nullable=False,index=True)
    position = Column(String(255),nullable=False)
    status = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "status in ('applied', 'interview', 'offer', 'selected', 'rejected', 'ghosted')",
            name='valid_application_status',
        ),

    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)



