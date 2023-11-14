from database import connection
from app.models.TransactionModel import Transaction
import logging

class TransactionServices():
    #get
    @classmethod
    def get_all_transactions(cls):
        """
        Get all transactions from DB
        
        Input: No need input

        Output:
        - TransactionModel's list 
        - 200, if operation is successfull
        - if exist error return dictionary with error mensage and HTTP 500

        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM transactions')
                result = cursor.fetchall()
                transactions = [Transaction(
                    transaction['id'],
                    transaction['title'],
                    transaction['date'],
                    transaction['amount'],
                    transaction['type'],
                    transaction['account_id'],
                    transaction['category_id']
                    ) for transaction in result]
            return transactions, 200
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    
    @classmethod
    def delete_all_transactions(cls):
        """
        Delete all transaction in DB
        
        Input: No need input

        Output:
        - dictionary with successful message and 200 if operation is successfull
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM transactions')
            connection.commit()
            return {'message':'Transacciones eliminadas exitosamente'}, 200
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    
    #post
    @classmethod
    def create_transaction(cls, transaction: Transaction):
        """
        Create transaction in DB
        
        Input: TransactionModel -> transaction
            - transaction.id -> int
            - transaction.title -> str
            - transaction.date -> date
            - transaction.amount -> int
            - transaction.type -> ENUM
            - transaction.account_id -> int
            - transaction.category_id -> int

        Output:
        - dictionary with message successfull and 201 if operation is successfull
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO transactions (title, date, amount, type, account_id, category_id) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % 
                    (transaction.title,
                    transaction.date.strftime('%Y-%m-%d'),
                    str(transaction.amount),
                    str(transaction.type),
                    str(transaction.account_id),
                    str(transaction.category_id))
                    )
            connection.commit()
            return {'message':"Transacción creada exitosamente"}, 201
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    #get id
    @classmethod
    def get_transaction(cls, id: int):
        """
        Get one transaction by id from DB
        
        Input: transaction's id

        Output:
        - TransactionModel with transaction's information
        - 200, if operation is successfull
        - if account is not found return dictionary with error mensage and HTTP 404
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM transactions WHERE id={str(id)}')
                result = cursor.fetchone()
                if result:
                    transaction = Transaction(
                        result['id'],
                        result['title'],
                        result['date'],
                        result['amount'],
                        result['type'],
                        result['account_id'],
                        result['category_id']
                        )
                    return transaction, 200
                else:
                    return {'error':'Transacción no encontrada'}, 404
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    #put id
    @classmethod
    def update_transaction(cls, id: int, transaction: Transaction):
        """
        Update transaction by id in DB
        
        Input: 
        - id: int transaction's id
        - TransactionModel with updated information
            - transaction.id -> int
            - transaction.title -> str
            - transaction.date -> date
            - transaction.amount -> int
            - transaction.type -> ENUM
            - transaction.account_id -> int
            - transaction.category_id -> int

        Output:
        - dictionary with successful message and 201 if operation is successfull
        - if tramsaction is not found return dictionary with error mensage and HTTP 404
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            if not cls.transaction_exists(id):
                return {"error": "La transacción no fue encontrada."}, 404
            
            with connection.cursor() as cursor:
                cursor.execute(
                    'UPDATE transactions SET title = "%s", date = "%s", amount = "%s", type = "%s", account_id = "%s", category_id = "%s" WHERE id = %s' % 
                    (transaction.title,
                    transaction.date.strftime('%Y-%m-%d'),
                    str(transaction.amount),
                    str(transaction.type),
                    str(transaction.account_id),
                    str(transaction.category_id), 
                    str(id))
                    )
            connection.commit()
            return {'message':'Transacción actualizada exitosamente'}, 200
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    #delete id
    @classmethod
    def delete_transaction(cls, id: int):
        """
        Delete transaction by id in DB
        
        Input: transaction's id

        Output:
        - dictionary with successful message and 200 if operation is successfull
        - if account is not found return dictionary with error mensage and HTTP 404
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            if not cls.transaction_exists(id):
                return {"error": "La transacción no fue encontrada."}, 404
            
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM transactions WHERE id = %s' % (str(id)))
            connection.commit()
            return {'message':'Transacción eliminada exitosamente'}, 200
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    



    @classmethod
    def transaction_exists(cls, id: int):
        '''
        Verify if transaction exist

        Input: id
        
        Output:
        - True if exist
        - False if not exist or if exception occurs
        
        '''
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT id FROM transactions WHERE id = %s' % (str(id)))
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            logging.debug(e)
            return False