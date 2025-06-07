from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database model
class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR)

# Database model
class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR)
    student_count = Column(Integer)
    teacher_id = Column(Integer)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TeacherResponse(BaseModel):
    id: int
    name: str

class TeacherCreate(BaseModel):
    name: str

@app.get("/teachers")
async def read_teachers(db: Session = Depends(get_db)) -> list[TeacherResponse]:
    db_teachers = db.query(Teacher)
    if db_teachers is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_teachers

@app.post("/teachers", response_model=TeacherCreate)
async def create_teachers(item: TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = Teacher(**item.model_dump())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@app.get("/teachers/{item_id}/courses", response_model=list[TeacherResponse])
async def read_teacher_courses(item_id: int, db: Session = Depends(get_db)):
    db_items = db.query(Course).filter(Course.teacher_id == item_id)
    if db_items.first() is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_items

@app.delete("/teachers/{id}")
def delete_teacher(id: int,db: Session=Depends(get_db)):

    found_teacher = db.query(Teacher).filter(Teacher.id==id)
    if found_teacher.first() == None:
        raise HTTPException(status_code=404, detail=f"post with {id} not found!")

    found_teacher.delete(synchronize_session=False)
    db.commit()
    return found_teacher

class CourseResponse(BaseModel):
    id: int
    name: str
    student_count: int
    teacher_id: int

class CourseCreate(BaseModel):
    name: str
    student_count: int
    teacher_id: int

@app.get("/courses")
async def read_courses(db: Session = Depends(get_db)) -> list[CourseResponse]:
    db_courses = db.query(Course)
    if db_courses is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_courses

@app.post("/courses", response_model=CourseCreate)
async def create_course(item: CourseCreate, db: Session = Depends(get_db)):
    db_courses = Course(**item.model_dump())
    db.add(db_courses)
    db.commit()
    db.refresh(db_courses)
    return db_courses

@app.delete("/courses/{id}")
def delete_course(id: int,db: Session=Depends(get_db)):

    found_course = db.query(Course).filter(Course.id==id)
    if found_course.first() == None:
        raise HTTPException(status_code=404, detail=f"post with {id} not found!")

    found_course.delete(synchronize_session=False)
    db.commit()
    return found_course

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)