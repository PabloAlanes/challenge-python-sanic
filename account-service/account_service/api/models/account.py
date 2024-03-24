from mongoengine import IntField, Document, EmbeddedDocumentField
from account_service.api.models.user import UserModel


class AccountModel(Document):
    money = IntField(default=0)
    user = EmbeddedDocumentField(UserModel)

    def to_dict(self):
        return {
            'id': str(self.id),
            'user': f'{self.user.first_name} {self.user.last_name}',
            'money': self.money
        }
