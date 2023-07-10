from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from routes.project import blp as ProjectBlueprint
from routes.user import blp as UserBlueprint
from routes.task import blp as TaskBlueprint
from database import db

def create_app():
        app = Flask(__name__)
        app.config["API_TITLE"] = "HR MANAGEMENT REST API"
        app.config["API_VERSION"] = "v1"
        app.config["OPENAPI_VERSION"] = "3.0.3"
        app.config["OPENAPI_URL_PREFIX"] = "/"
        app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
        app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abhi8477@0.tcp.in.ngrok.io:19784/HRM'
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
        app.config["JWY_REFRESH_TOKEN_EXPIRES"] = 172800
        app.config["JWT_SECRET_KEY"] = "secret"
        db.init_app(app)

        api = Api(app)
        jwt = JWTManager(app)

        with app.app_context():
                db.create_all()
                
        api.register_blueprint(ProjectBlueprint)
        api.register_blueprint(UserBlueprint)
        api.register_blueprint(TaskBlueprint)
        return app

app = create_app()
app.run("0.0.0.0",5000,debug=True)