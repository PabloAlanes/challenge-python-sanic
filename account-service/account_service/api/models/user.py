from mongoengine import StringField, EmailField, EmbeddedDocument


class UserModel(EmbeddedDocument):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField()

    openapi_schema = {
        'type': 'object',
        'required': ['first_name', 'last_name'],
        'properties': {
            'email': { 'type': 'integer', 'format': 'email' },
            'first_name': { 'type': 'string' },
            'last_name': { 'type': 'string' }
        }
    }
