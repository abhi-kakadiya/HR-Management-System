from database import db
from models.model import ProjectModel, UserModel, UserProjectModel
from flask.views import MethodView
from flask import jsonify
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.project_schema import CreateProject, DisplayProject, UpdateProject, AssignSchema


blp = Blueprint("Project", __name__, description="Operations for projects")


@blp.route("/projects")
class ProjectApi_CR(MethodView):

    @jwt_required()
    @blp.response(200, DisplayProject(many=True))
    def get(self):
        projects = ProjectModel.query.all()
        if projects:      
            return projects
        else:
            abort(jsonify(code=400, message="No projects found"))

    @jwt_required()
    @blp.arguments(CreateProject)
    @blp.response(201, DisplayProject)
    def post(self, request_data):

        current_user_id = get_jwt_identity()
        if UserModel.query.filter_by(id=current_user_id, role="ADMIN").first():

            project_query = ProjectModel.query.filter_by(title=request_data['title']).first()
            if project_query:
                abort(jsonify(code=400, message=f"Project with title '{request_data['title']}' already exists"))

            else:
                project = ProjectModel(
                    title = request_data['title'],
                    status = request_data['status']
                )
                db.session.add(project)
                db.session.commit()

                return project
        else:
            abort(jsonify(code=401, message=f"Admin access required!"))



@blp.route("/project/<int:project_id>") 
class ProjectApi_UD(MethodView):

    @jwt_required()
    @blp.response(200, DisplayProject)
    def get(self, project_id):
        
        current_user_id = get_jwt_identity()
        if UserModel.query.filter_by(id=current_user_id, role="ADMIN").first():
            project = ProjectModel.query.filter_by(id=project_id).first()
            if project:
                return project
            else:
                abort(jsonify(code=404, message=f"Project with id '{project_id}' does not exists"))
        else:
            abort(jsonify(code=401, message=f"Admin access required!"))


    @jwt_required()
    @blp.arguments(UpdateProject)
    @blp.response(201, DisplayProject)
    def put(self, update_data, project_id):

        current_user_id = get_jwt_identity()
        if UserModel.query.filter_by(id=current_user_id, role="ADMIN").first():
            project = ProjectModel.query.filter_by(id=project_id).first()
            if project:
                ProjectModel.query.filter_by(id=project_id).update(update_data)
                db.session.commit()
                updated_project = ProjectModel.query.get(project_id)
                return updated_project
            else:
                abort(jsonify(code=404, message=f"Project with id '{project_id}' does not exists"))
        else:
            abort(jsonify(code=401, message=f"Admin access required!"))


    @jwt_required()
    def delete(self, project_id):

        current_user_id = get_jwt_identity()
        if UserModel.query.filter_by(id=current_user_id, role="ADMIN").first():
            project = ProjectModel.query.filter_by(id=project_id).first()
            if project:
                db.session.delete(project)
                db.session.commit()
                return {"message": f"Project with id '{project_id}' has been deleted"}
            else:
                abort(jsonify(code=404, message=f"Project with id '{project_id}' does not exists"))
        else:
            abort(jsonify(code=401, message=f"Admin access required!"))





@blp.route("/project/assign")
class AssignDeveloper(MethodView):
    
    @jwt_required()
    @blp.arguments(AssignSchema)
    def post(self, request_data):
        
        current_user_id = get_jwt_identity()
        if UserModel.query.filter_by(id=current_user_id, role="ADMIN").first():
            project = ProjectModel.query.filter_by(id = request_data['project_id']).first()
            developer = UserModel.query.filter_by(id = request_data['developer_id']).first()
            
            if str(developer.role) == "ADMIN":
                abort(jsonify(code=400, message=f'User with id {developer.id} is not Developer'))
            
            if project and developer:
                if UserProjectModel.query.filter_by(project_id = project.id, developer_id = developer.id).first():
                    abort(jsonify(code=400, message=f'Developer with id {developer.id} is already assigned to project {project.id}'))
                else:    
                    project.developers.append(developer)
                    db.session.commit()
                    return {"message": f"Developer with id {developer.id} has been assigned to project {project.id}"}
        else:
             abort(jsonify(code=401, message=f"Admin access required!"))
            