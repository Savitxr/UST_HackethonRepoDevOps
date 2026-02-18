from models import deletedrowsDB,TaskDB
from database import engine , base ,sessionlocal
from sqlalchemy.orm import Session
from fastapi import FastAPI , Depends ,Query , HTTPException
from pydantic import BaseModel , field_validator
from datetime import date,datetime
from enum import Enum
from fastapi.responses import JSONResponse

app=FastAPI(title="Personal Task Management Web Application")
base.metadata.create_all(bind=engine)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "timestamp": datetime.utcnow().isoformat(),
            "status": exc.status_code,
            "message": exc.detail,
            "path": request.url.path
        }
    )

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()

class statusvalues(str, Enum):
    PENDING="PENDING"
    COMPLETED="COMPLETED"

class TaskCreate(BaseModel):
    name: str
    description: str
    dueDate: date
    status: statusvalues=statusvalues.PENDING

    @field_validator("name")
    @classmethod
    def check_name_not_empty(cls,v):
        if v.strip()=="" or v.strip()=="string":
            raise ValueError("Name cannot be left empty")
        return v
    
    @field_validator("dueDate")
    @classmethod
    def check_due_dat(cls,v):
        if v < date.today():
            raise ValueError("Due date canot be in Past")
        return v
            
    @field_validator("description")
    @classmethod
    def check_description_not_empty(cls,v):
        if v.strip()=="" or v.strip().lower()=="string":
            raise ValueError("description cannot be left empty")
        return v



class TaskResponse(TaskCreate):
    id :int

    class Config:
        from_attributes=True

class DeletedRowsResponse(BaseModel):
    id:int
    Original_id:int
    name: str
    description: str
    dueDate: date
    status: statusvalues

    class Config:
        from_attributes=True

@app.get('/')
def root():
    return f"Task Management Web Application"

@app.post('/api/v1/tasks', response_model=TaskResponse)
def create_task(item:TaskCreate , db:Session=Depends(get_db)):
    db_item=TaskDB(name=item.name, description=item.description,dueDate=item.dueDate , status=item.status)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get('/api/v1/tasks', response_model=list[TaskResponse])
def retrieve_tasks( db:Session=Depends(get_db)):
    return db.query(TaskDB).all()
@app.get('/api/v1/tasks/status', response_model=list[TaskResponse])
def retrive_tasks_by_status(status:statusvalues, db:Session=Depends(get_db)):
    return db.query(TaskDB).filter(TaskDB.status==status).all()

@app.get('/api/v1/tasks/overdue', response_model=list[TaskResponse])
def retrive_overdue_tasks( db:Session=Depends(get_db)):
    return db.query(TaskDB).filter(TaskDB.dueDate<date.today(), TaskDB.status==statusvalues.PENDING).all()

@app.get('/api/v1/tasks/sort', response_model=list[TaskResponse])
def retrive_sorted_tasks(db:Session=Depends(get_db)):
    return db.query(TaskDB).order_by(TaskDB.dueDate).all()

@app.get('/api/v1/tasks/deleted', response_model=list[TaskResponse])
def retrive_deleted_tasks(db:Session=Depends(get_db)):
    return db.query(deletedrowsDB).all()

@app.get('/api/v1/tasks/{id}', response_model=TaskResponse)
def retrieve_task(id:int, db:Session=Depends(get_db)):
    return db.query(TaskDB).filter(TaskDB.id==id).first()

@app.put('/api/v1/tasks/{id}', response_model=TaskResponse)
def update_task(id:int,item:TaskCreate , db:Session=Depends(get_db)):
    row=db.query(TaskDB).filter(TaskDB.id==id).first()
    if row:
        row.name=item.name
        row.description=item.description
        row.dueDate=item.dueDate
        row.status=item.status
    else:
        raise HTTPException(status_code=404, detail="row not found")
    db.commit()
    db.refresh(row)
    return row


@app.delete('/api/v1/tasks/{id}', response_model=DeletedRowsResponse)
def delete_task(id:int, db:Session=Depends(get_db)):
    row=db.query(TaskDB).filter(TaskDB.id==id).first()
    if row:
        db_item=deletedrowsDB(Original_id=row.id, name=row.name, description=row.description,dueDate=row.dueDate, status=row.status)
    else:
        raise HTTPException(status_code=404, detail="row not found")
    db.add(db_item)
    db.delete(row)
    db.commit()
    db.refresh(db_item)
    return db_item
