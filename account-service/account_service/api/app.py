from sanic import Sanic
from account_service.api.views.account import AccountView

# Sanic setup
app = Sanic("AcountService")
app.add_route(AccountView.as_view(), "/accounts/<id:strorempty>/")