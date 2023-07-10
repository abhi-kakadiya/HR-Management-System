from marshmallow import Schema, fields


class DeveloperDetails(Schema):
    name = fields.Str()
    email = fields.Email()


class CreateProject(Schema):
    title = fields.Str(required=True)
    status = fields.Str(required=True)


class DisplayProject(Schema):
    id = fields.Int()
    title = fields.Str()
    status = fields.Str()
    developers = fields.List(fields.Nested(DeveloperDetails), dump_only=True)


class UpdateProject(Schema):
    title = fields.Str()
    status = fields.Str()

class AssignSchema(Schema):
    project_id = fields.Int(required=True)
    developer_id = fields.Int(required=True)
    