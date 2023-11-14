from flask import request, jsonify, Blueprint
from app.models.TransactionModel import Transaction
from app.services.TransactionServices import TransactionServices
from app.utils.Transaction_to_json import Transaction_to_json
from app .utils.Transaction_input_verify import verify
from datetime import datetime



transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions', methods=['GET','POST', 'DELETE'])
def transactions():
    if request.method == 'GET':
        transactions_response = TransactionServices.get_all_transactions()
        if transactions_response[1]==200:
            transactions = [Transaction_to_json(transaction) for transaction in transactions_response[0]]
            transactions_response = (transactions,transactions_response[1])
        return jsonify(transactions_response[0]), transactions_response[1]
    elif request.method == 'POST':
        title, date, amount, type, account_id, category_id = verify(
            request.json.get('title'),
            request.json.get('date'),
            request.json.get('amount'),
            request.json.get('type'),
            request.json.get('account_id'),
            request.json.get('category_id'))
        new_transaction = Transaction(0, title, date,amount,type,account_id,category_id)
        response = TransactionServices.create_transaction(new_transaction)
        return jsonify(response[0]), response[1]
    else:
        response = TransactionServices.delete_all_transactions()
        return jsonify(response[0]), response[1]

@transactions_bp.route('/transactions/<int:id>', methods=['GET','PUT', 'DELETE'])
def transactions_id(id):
    if request.method == 'GET':
        response = TransactionServices.get_transaction(id)
        print(response)
        if response[1]==200:
            response = (Transaction_to_json(response[0]),response[1])
        return jsonify(response[0]), response[1]
    elif request.method == 'PUT':
        title, date, amount, type, account_id, category_id = verify(
            request.json.get('title'),
            request.json.get('date'),
            request.json.get('amount'),
            request.json.get('type'),
            request.json.get('account_id'),
            request.json.get('category_id'))
        updated_transaction = Transaction(id, title, date, amount, type, account_id, category_id)
        response = TransactionServices.update_transaction(id, updated_transaction)
        print(response)
        return jsonify(response[0]), response[1]
    else:
        response = TransactionServices.delete_transaction(id)
        return jsonify(response[0]), response[1]