from app.models.TransactionModel import Transaction

def Transaction_to_json(transaction: Transaction):
    json = {
        'id': transaction.id,
        'title': transaction.title,
        'date': transaction.date.strftime('%Y-%m-%d'),
        'amount': transaction.amount,
        'type': transaction.type,
        'account_id': transaction.account_id,
        'category_id': transaction.category_id,
    }
    return json