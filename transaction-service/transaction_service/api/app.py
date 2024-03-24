from sanic import Sanic
from transaction_service.api.views.transaction import TransactionView

# Sanic setup
app = Sanic("TransactionService")
app.add_route(TransactionView.as_view(), "/transactions/<id:strorempty>/")