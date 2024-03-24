import json
import mongomock
import pytest
import unittest

from sanic_testing.testing import SanicTestClient
from mongoengine import connect, disconnect, DoesNotExist
from transaction_service.api.app import app
from transaction_service.api.models.transaction import TransactionModel, Status
from http import HTTPStatus


class TestTransaction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('db', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)
        cls.test_client = SanicTestClient(app)

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_create_transaction(self):
        request, response = self.test_client.post('/transactions/', json={
            'source_account': 'a',
            'destiny_account': 'b',
            'amount': 10
        })
        assert response.status == HTTPStatus.ACCEPTED
        resp_body = json.loads(response.body)
        assert resp_body['source'] == 'a'
        assert resp_body['destiny'] == 'b'
        assert resp_body['amount'] == 10
        assert resp_body['status'] == Status.PENDING.value

    def test_create_transaction_invalid(self):
        request, response = self.test_client.post('/transactions/', json={
            'source_account': 'a',
            'destiny_account': 'b',
        })
        assert response.status == HTTPStatus.BAD_REQUEST

    def test_get_transaction(self):
        transaction = TransactionModel(
            source_account='a',
            destiny_account='b',
            amount=10
        )
        transaction.save()
        request, response = self.test_client.get(f'/transactions/{transaction.id}')
        assert response.status == HTTPStatus.OK
        resp_body = json.loads(response.body)
        assert resp_body['source'] == 'a'
        assert resp_body['destiny'] == 'b'
        assert resp_body['amount'] == 10
        assert resp_body['status'] == Status.UNDEFINED.value

    def test_get_transaction_that_not_exist(self):
        request, response = self.test_client.get('/transactions/65f8cc0a7adc8b14a36d01a0')
        assert response.status == HTTPStatus.NOT_FOUND

    def test_put_transaction(self):
        transaction = TransactionModel(
            source_account='a',
            destiny_account='b',
            amount=10
        )
        transaction.save()

        request, response = self.test_client.put(f'/transactions/{transaction.id}',
                                                 json={'status': Status.DONE.value})
        assert response.status == HTTPStatus.NO_CONTENT
        transaction_updated = TransactionModel.objects.get(id=transaction.id)
        assert transaction_updated.status == Status.DONE

    def test_put_transaction_that_not_exist(self):
        request, response = self.test_client.put(f'/transactions/65f8cc0a7adc8b14a36d01a0', json={'money': 2})
        assert response.status == HTTPStatus.NOT_FOUND

    def test_delete_transaction(self):
        transaction = TransactionModel(
            source_account='a',
            destiny_account='b',
            amount=10
        )
        transaction.save()

        request, response = self.test_client.delete(f'/transactions/{transaction.id}')
        assert response.status == HTTPStatus.NO_CONTENT

        with pytest.raises(DoesNotExist):
            TransactionModel.objects.get(id=transaction.id)

    def test_delete_transaction_that_not_exist(self):
        request, response = self.test_client.delete('/transactions/65f8cc0a7adc8b14a36d01a0')
        assert response.status == HTTPStatus.NOT_FOUND
