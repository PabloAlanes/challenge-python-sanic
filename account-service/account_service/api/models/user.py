from mongoengine import StringField, EmailField, EmbeddedDocument


class UserModel(EmbeddedDocument):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField()

