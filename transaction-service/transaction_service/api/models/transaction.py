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

    openapi_schema = {
        'type': 'object',
        'required': ['source_account', 'destiny_account', 'amount'],
        'properties': {
            'source_account': {'type': 'string'},
            'destiny_account': {'type': 'string'},
            'amount': {'type': 'integer', 'format': 'int32', 'minimum': 0},
            'create_at': {'type': 'string', 'format': 'date-time'},
            'status': {
                'type': 'string',
                'enum': ['done', 'pending', 'undefined', 'error'],
                "default": "undefined"
            },
        }
    }
