from marshmallow import Schema, fields
from schemas.project_schema import DeveloperDetails

class CreateTask(Schema):
        name = fields.Str(required=True)
        priority = fields.Int(required=True)
        duration = fields.TimeDelta(required=True)
        developer_id = fields.Int(required=True)
        
class DisplayTask(Schema):
        id = fields.Int()
        name = fields.Str()
        priority = fields.Int()
        duration = fields.TimeDelta()
        developer = fields.Nested(DeveloperDetails, dump_only=True)

class UpdateTask(Schema):
        name = fields.Str()
        priority = fields.Int()
        duration = fields.TimeDelta()
        
        