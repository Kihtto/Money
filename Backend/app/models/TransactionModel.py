from datetime import datetime
class Transaction():
    def __init__(self, id: int, title: str, date: datetime, amount: int, type: str, account_id: int, category_id: int) -> None:
        self.id = id
        self.title = title
        self.date = date
        self.amount = amount
        self.type = type
        self.account_id = account_id
        self.category_id = category_id