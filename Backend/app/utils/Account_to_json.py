from app.models.AccountModel import Account

def Account_to_json(account: Account):
    json = {
        'id': account.id,
        'title': account.title,
        'initial_balance': account.initial_balance
    }
    return json