from database import db
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from datetime import timedelta
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.task_schema import CreateTask, DisplayTask, UpdateTask
from models.model import TaskModel, UserModel

blp = Blueprint("Task", __name__, description="Operations for tasks")

@blp.route("/task")
class TaskApi_CR(MethodView):
        
        @jwt_required()
        @blp.arguments(CreateTask)
        @blp.response(201, DisplayTask)
        def post(self, task_data):
                
                current_user_id = get_jwt_identity()
                if UserModel.query.filter_by(id = current_user_id, role = "DEVELOPER").first():
                        if TaskModel.query.filter_by(name = task_data['name'], \
                                developer_id = task_data['developer_id']).first():
                                abort(jsonify(code=400, message=f"Task is already assigned to Developer with ID {task_data['developer_id']}"))
                        else:
                                task = TaskModel(**task_data) 
                                db.session.add(task)
                                db.session.commit()
                                return task     
                else:
                        abort(jsonify(code=401, message=f"Developer access required!"))
        
        @jwt_required()                        
        @blp.response(200, DisplayTask(many=True))                  
        def get(self):
                
                current_user_id = get_jwt_identity()
                if UserModel.query.filter_by(id = current_user_id, role = "ADMIN").first():
                        tasks = TaskModel.query.all()
                        if tasks:
                                return tasks
                        else:
                                abort(jsonify(code=400, message="No Tasks found"))
                else:
                        abort(jsonify(code=401, message=f"Admin access required!"))        
                
                        
@blp.route("/developer/<int:developer_id>/task")
class TaskApi_R(MethodView):
        
        @jwt_required()
        @blp.response(200, UpdateTask(many=True))
        def get(self, developer_id):
                
                current_user_id = get_jwt_identity()
                if UserModel.query.filter_by(id = current_user_id, role = "DEVELOPER").first():
                        tasks = TaskModel.query.filter_by(developer_id=developer_id).all()
                        if tasks:
                                return tasks
                        else:
                                abort(jsonify(code=404, message=f"Developer with id {developer_id} does not have any tasks"))
                else:
                        abort(jsonify(code=401, message=f"Developer access required!"))
	

@blp.route("/task/<int:task_id>")
class TaskApi_UD(MethodView):
        
        @jwt_required()
        @blp.arguments(UpdateTask)
        @blp.response(201, DisplayTask)
        def put(self, update_data, task_id):
                
                current_user_id = get_jwt_identity()
                if UserModel.query.filter_by(id = current_user_id, role = "DEVELOPER").first():
                        task = TaskModel.query.filter_by(id=task_id).first()
                        if task:
                                TaskModel.query.filter_by(id=task_id).update(update_data)
                                db.session.commit()
                                updated_task = TaskModel.query.get(task_id)
                                return updated_task
                        else:
                                abort(jsonify(code=404, message=f"Task with id {task_id} does not exists"))
                else:
                        abort(jsonify(code=401, message=f"Developer access required!"))
                
        
        @jwt_required()
        def delete(self, task_id):
                
                current_user_id = get_jwt_identity()
                if UserModel.query.filter_by(id = current_user_id, role = "DEVELOPER").first():
                        task = TaskModel.query.filter_by(id=task_id).first()
                        if task:
                                db.session.delete(task)
                                db.session.commit()
                                return {"message": f"Project with id {task_id} has been deleted"}
                        else:
                                abort(jsonify(code=404, message=f"Task with id {task_id} does not exists"))
                else:
                        abort(jsonify(code=401, message=f"Developer access required!"))
                
                