from database import db
from sqlalchemy import Interval
import datetime
import enum

class ProjectStatus(enum.Enum):
        RUNNING = 'RUNNING'
        COMPLETED = 'COMPLETED'
        ONHOLD = 'ONHOLD'
        UNDERREVIEW = 'UNDERREVIEW'

        def __str__(self):
 	       return self.value

class UserRole(enum.Enum):
        ADMIN = "ADMIN"
        DEVELOPER = "DEVELOPER"
        
        def __str__(self):
 	       return self.value
        


class UserProjectModel(db.Model):
        __tablename__ = "user_project"
        
        id = db.Column(db.Integer, primary_key=True)
        developer_id = db.Column(db.Integer, db.ForeignKey("users.id"))        
        project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))


class UserModel(db.Model):
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), default=None )
        email = db.Column(db.String(255), unique=True, nullable=False)
        role = db.Column(db.Enum(UserRole))        
        password = db.Column(db.String(255), nullable=False)
        
        projects = db.relationship("ProjectModel", back_populates="developers", secondary="user_project")
        tasks = db.relationship("TaskModel", back_populates="developer")

class ProjectModel(db.Model):
        __tablename__ = "projects"
        
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(255), nullable=False)
        status = db.Column(db.Enum(ProjectStatus), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.datetime.now)
	
        developers = db.relationship("UserModel", back_populates="projects", secondary="user_project")

                
class TaskModel(db.Model):
        __tablename__ = 'tasks'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), nullable=False)
        priority = db.Column(db.Integer, nullable=False)
        duration = db.Column(Interval, nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.datetime.now)
        developer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        
        developer = db.relationship("UserModel", back_populates="tasks")
