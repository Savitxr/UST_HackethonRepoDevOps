from database import base, engine
from sqlalchemy import Column , String , Integer , Enum , DATE
import enum


class statusvalues(enum.Enum):
    PENDING="PENDING"
    COMPLETED="COMPLETED"

class TaskDB(base):
    __tablename__="Task"
    id=Column(Integer, primary_key=True , autoincrement= True  )
    name=Column(String , nullable=False)
    description=Column(String , nullable=False)
    dueDate=Column(DATE , nullable=False)
    status=Column(Enum(statusvalues),default=statusvalues.PENDING)


class deletedrowsDB(base):
    __tablename__="deletedrows"
    id=Column(Integer , primary_key=True, autoincrement=True)
    Original_id=Column(Integer)
    name=Column(String , nullable=False)
    description=Column(String , nullable=False)
    dueDate=Column(DATE , nullable=False)
    status=Column(Enum(statusvalues))