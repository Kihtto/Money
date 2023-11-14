from database import connection
from app.models.AccountModel import Account
import logging


class AccountServices():
    #get
    @classmethod
    def get_all_accounts(cls):
        """
        Get all accounts from DB
        
        Input: No need input

        Output:
        - Account's object list 
        - 200, if operation is successfull
        - if exist error return dictionary with error mensage and HTTP 500

        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM accounts')
                result = cursor.fetchall()
                accounts = [Account(account['id'],account['title'],account['initial_balance']) for account in result]
            return accounts, 200
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    #delete
    @classmethod
    def delete_all_acounts(cls):
        """
        Delete all account in DB
        
        Input: No need input

        Output:
        - dictionary with successful message and 200 if operation is successfull
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM accounts')
            connection.commit()
            return {'message':'Cuentas eliminadas exitosamente'}, 200
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    #post
    @classmethod
    def create_account(cls, account: Account):
        """
        Create account in DB
        
        Input: Account object
            - account.title -> str
            - account.initial_balance int

        Output:
        - dictionary with message successfull and 201 if operation is successfull
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO accounts (title, initial_balance) VALUES ('%s', '%s')" % 
                    (account.title, account.initial_balance))
            connection.commit()
            return {'message':"Cuenta creada exitosamente"}, 201
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    #get id
    @classmethod
    def get_account(cls, id: int):
        """
        Get one account by id from DB
        
        Input: account's id

        Output:
        - Account object with account's information, 200, if operation is successfull
        - If id is not found return 404
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM accounts WHERE id={str(id)}')
                result = cursor.fetchone()
                if result:
                    account = Account(
                        result['id'],
                        result['title'],
                        result['initial_balance'],
                        )
                    return account, 200
                else:
                    return {'error':'Cuenta no encontrada'}, 404
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    #put id
    @classmethod
    def update_account(cls, id: int, account: Account):
        """
        Update account by id in DB
        
        Input: 
        - id: int account's id
        - Account object with updated information 
            - account.title -> str
            - account.initial_balance. int

        Output:
        - dictionary with successful message and 201 if operation is successfull
        - if account is not found return dictionary with error mensage and HTTP 404
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            if not cls.account_exists(id):
                return {"error": "La cuenta no fue encontrada."}, 404
            
            with connection.cursor() as cursor:
                cursor.execute(
                    'UPDATE accounts SET title = "%s", initial_balance = "%s" WHERE id = %s' % 
                    (account.title, account.initial_balance, str(id)))
            connection.commit()
            return {'message':'Cuenta actualizada exitosamente'}, 200
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    #delete id
    @classmethod
    def delete_account(cls, id: int):
        """
        Delete account by id in DB
        
        Input: account's id

        Output:
        - dictionary with successful message and 200 if operation is successfull
        - if account is not found return dictionary with error mensage and HTTP 404
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            if not cls.account_exists(id):
                return {"error": "La cuenta no fue encontrada."}, 404
            
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM accounts WHERE id = %s' % (str(id)))
            connection.commit()
            return {'message':'Cuenta eliminada exitosamente'}, 200
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    



    @classmethod
    def account_exists(cls, id: int):
        '''
        Verify if account exist

        Input: id
        
        Output:
        - True if exist
        - False if not exist or if exception occurs
        
        '''
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT id FROM accounts WHERE id = %s' % (str(id)))
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            logging.debug(e)
            return False