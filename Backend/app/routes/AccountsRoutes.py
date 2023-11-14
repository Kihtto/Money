from flask import request, jsonify, Blueprint
from app.models.AccountModel import Account
from app.services.AccountsServices import AccountServices
from app.utils.Account_to_json import Account_to_json
from app.utils.Account_input_verify import verify


accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/accounts', methods=['GET','POST', 'DELETE'])
def accounts():
    if request.method == 'GET':
        accounts_response = AccountServices.get_all_accounts()
        if accounts_response[1]==200:
            accounts = [Account_to_json(account) for account in accounts_response[0]]
            accounts_response = (accounts,accounts_response[1])
        return jsonify(accounts_response[0]), accounts_response[1]
    elif request.method == 'POST':
        title, initial_balance = verify(
            request.json.get('title'),
            request.json.get('initial_balance'),)
        new_account = Account(0, title, initial_balance)
        response = AccountServices.create_account(new_account)
        return jsonify(response[0]), response[1]
    else:
        response = AccountServices.delete_all_acounts()
        return jsonify(response[0]), response[1]

@accounts_bp.route('/accounts/<int:id>', methods=['GET','PUT', 'DELETE'])
def accounts_id(id):
    if request.method == 'GET':
        response = AccountServices.get_account(id)
        if response[1]==200:
            response = (Account_to_json(response[0]),response[1])
        return jsonify(response[0]), response[1]
    elif request.method == 'PUT':
        title, initial_balance = verify(
            request.json.get('title'),
            request.json.get('initial_balance'),)
        updated_account = Account(id, title, initial_balance)
        response = AccountServices.update_account(id, updated_account)
        return jsonify(response[0]), response[1]
    else:
        response = AccountServices.delete_account(id)
        return jsonify(response[0]), response[1]