from . import app, db
from . import views

app.add_url_rule('/transaction/create', view_func=views.transaction_create, methods=['POST', 'GET'])
app.add_url_rule('/transaction/list', view_func=views.transaction_list)
app.add_url_rule('/transaction/<int:transaction_id>/update', view_func=views.transaction_update, methods=['POST', 'GET'])
app.add_url_rule('/transaction/<int:transaction_id>/delete', view_func=views.transaction_delete, methods=['POST', 'GET'])

app.add_url_rule('/account/register', view_func=views.user_register, methods=['POST', 'GET'])
app.add_url_rule('/account/login', view_func=views.user_login, methods=['POST', 'GET'])
app.add_url_rule('/account/logout', view_func=views.user_logout)