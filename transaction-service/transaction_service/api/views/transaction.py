from sanic import json
from sanic.views import HTTPMethodView
from sanic_ext import openapi
from transaction_service.api.models.transaction import TransactionModel, Status
from transaction_service.utils.handler_errors import HandlerError
from http import HTTPStatus

class TransactionView(HTTPMethodView):

    @openapi.summary('Get data from all transactions or a transaction')
    @openapi.parameter('id', required=False, allowEmptyValue=True, location='path')
    @HandlerError
    async def get(self, id):
        if not id:
            transactions = [t.to_dict() for t in TransactionModel.objects]
            return json(transactions, status=HTTPStatus.OK)

        transaction = TransactionModel.objects.get(id=id)
        return json(transaction.to_dict(), status=HTTPStatus.OK)

    @openapi.summary('Create a new transaction')
    @openapi.parameter('id', required=False, allowEmptyValue=True, deprecated=True)
    @openapi.body({'application/json': TransactionModel.openapi_schema})
    @HandlerError
    async def post(self, request, id):
        body = request.json
        transaction = TransactionModel(status=Status.PENDING, **body)
        transaction.save()
        return json(transaction.to_dict(), status=HTTPStatus.ACCEPTED)

    @openapi.summary('Update a transaction that already exist')
    @openapi.body({'application/json': TransactionModel.openapi_schema})
    @HandlerError
    async def put(self, request, id):
        body = request.json
        transaction = TransactionModel.objects.get(id=id)
        transaction.update(**body)
        return json({'message': 'the transaction was updated'}, status=HTTPStatus.NO_CONTENT)

    @openapi.summary('Delete a transaction')
    @HandlerError
    async def delete(self, id):
        transaction = TransactionModel.objects.get(id=id)
        transaction.delete()
        return json({'message': 'the transaction was deleted'}, status=HTTPStatus.NO_CONTENT)
