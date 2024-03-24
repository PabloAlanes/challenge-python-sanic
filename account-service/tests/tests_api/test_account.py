import json
import mongomock
import pytest
import unittest

from sanic_testing.testing import SanicTestClient
from mongoengine import connect, disconnect, DoesNotExist
from account_service.api.app import app
from account_service.api.models.account import AccountModel
from account_service.api.models.user import UserModel
from http import HTTPStatus


class TestAccount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connect('db', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)
        cls.test_client = SanicTestClient(app)

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_create_account(self):
        request, response = self.test_client.post('/accounts/', json={'money': 1, 'user': {
            'first_name': 'a', 'last_name': 'b'}})
        assert response.status == HTTPStatus.CREATED
        resp_body = json.loads(response.body)
        assert resp_body['user'] == 'a b'
        assert resp_body['money'] == 1

    def test_get_account(self):
        account = AccountModel(money=1, user=UserModel(first_name='a', last_name='b'))
        account.save()

        request, response = self.test_client.get(f'/accounts/{account.id}')
        assert response.status == HTTPStatus.OK
        resp_body = json.loads(response.body)
        assert resp_body['user'] == 'a b'
        assert resp_body['money'] == 1

    def test_put_account(self):
        account = AccountModel(money=1, user=UserModel(first_name='a', last_name='b'))
        account.save()

        request, response = self.test_client.put(f'/accounts/{account.id}', json={'money': 2})
        assert response.status == HTTPStatus.NO_CONTENT

        account_updated = AccountModel.objects.get(id=account.id)
        assert account_updated.money == 2

    def test_delete_account(self):
        account = AccountModel(money=1, user=UserModel(first_name='a', last_name='b'))
        account.save()

        request, response = self.test_client.delete(f'/accounts/{account.id}')
        assert response.status == HTTPStatus.NO_CONTENT

        with pytest.raises(DoesNotExist):
            AccountModel.objects.get(id=account.id)
