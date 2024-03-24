import datetime
from enum import Enum
from mongoengine import StringField, IntField, Document, DateTimeField, EnumField


class Status(Enum):
    PENDING = 'pending'
    DONE = 'done'
    ERROR = 'error'
    UNDEFINED = 'undefined'


class TransactionModel(Document):
    source_account = StringField(required=True)
    destiny_account = StringField(required=True)
    amount = IntField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    status = EnumField(Status, default=Status.UNDEFINED)

    def to_dict(self):
        return {
            'id': str(self.id),
            'source': self.source_account,
            'destiny': self.destiny_account,
            'amount': self.amount,
            'created_at': self.created_at.isoformat(),
            'status': self.status.value
        }

