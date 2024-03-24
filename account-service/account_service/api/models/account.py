from mongoengine import IntField, Document, EmbeddedDocumentField
from account_service.api.models.user import UserModel


class AccountModel(Document):
    money = IntField(default=0)
    user = EmbeddedDocumentField(UserModel)

    openapi_schema = {
        'type': 'object',
        'required': ['source_account', 'destiny_account', 'amount'],
        'properties': {
            'money': { 'type': 'integer', 'format': 'int32', 'minimum': 0 },
            'user': UserModel.openapi_schema
        }
    }

    def to_dict(self):
        return {
            'id': str(self.id),
            'user': f'{self.user.first_name} {self.user.last_name}',
            'money': self.money
        }
