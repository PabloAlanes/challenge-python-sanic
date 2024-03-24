from sanic.views import HTTPMethodView
from sanic import json
from account_service.api.models.account import AccountModel
from http import HTTPStatus


class AccountView(HTTPMethodView):

    async def get(self, id):
        if not id:
            accounts = [account.to_dict() for account in AccountModel.objects]
            return json(accounts, status=HTTPStatus.OK)
        account = AccountModel.objects.get(id=id)
        return json(account.to_dict(), status=HTTPStatus.OK)

    async def post(self, request, id):
        body = request.json
        account = AccountModel(**body)
        account.save()
        return json(account.to_dict(), status=HTTPStatus.CREATED)

    async def put(self, request, id):
        body = request.json
        account = AccountModel.objects.get(id=id)
        account.update(**body)
        return json({'message': 'the account was updated'}, status=HTTPStatus.NO_CONTENT)

    async def delete(self, id):
        account = AccountModel.objects.get(id=id)
        account.delete()
        return json({'message': 'the account was deleted'}, status=HTTPStatus.NO_CONTENT)
