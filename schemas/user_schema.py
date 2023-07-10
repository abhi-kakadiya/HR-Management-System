from marshmallow import Schema, fields

class ProjectDetails(Schema):
        title = fields.Str()
        status = fields.Str()     

class TaskDetails(Schema):
        name = fields.Str()
        priority = fields.Int()
        duration = fields.TimeDelta()
        
class AuthSchema(Schema):
        email = fields.Email(required=True)
        password = fields.Str(required=True)        
        
class CreateUser(Schema):
        name = fields.Str(required=True)
        email = fields.Email(required=True)
        role = fields.Str(required=True)
        password = fields.Str(required=True)        

class DisplayUser(Schema):
        id = fields.Int()
        email = fields.Email()
        name = fields.Str()
        role = fields.Str()
        projects = fields.List(fields.Nested(ProjectDetails), dump_only=True)
        tasks = fields.List(fields.Nested(TaskDetails), dump_only=True)
                
class Updateuser(Schema):
        name = fields.Str()
        role = fields.Str()
        
