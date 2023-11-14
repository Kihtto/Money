from database import connection
from app.models.CategoryModel import Category
import logging


class CategoryServices():
    #get
    @classmethod
    def get_all_categories(cls):
        """
        Get all categories from DB
        
        Input: No need input

        Output:
        - CategoryModel's list 
        - 200, if operation is successfull
        - if exist error return dictionary with error mensage and HTTP 500

        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM categories')
                result = cursor.fetchall()
                categories = [Category(category['id'],category['title'],category['type']) for category in result]
            return categories, 200
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    @classmethod
    def delete_all_categories(cls):
        """
        Delete all category in DB
        
        Input: No need input

        Output:
        - dictionary with message successfull and 200 if operation is successfull
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM categories')
            connection.commit()
            return {'message':'Categorias eliminadas exitosamente'}, 200
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    #post
    @classmethod
    def create_category(cls, category: Category):
        """
        Create category in DB
        
        Input: CategoryModel -> category
            - category.title -> str
            - category.type ENUM

        Output:
        - dictionary with message successfull and 201 if operation is successfull
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO categories (title, type) VALUES ('%s', '%s')" % 
                    (category.title, category.type))
            connection.commit()
            return {'message':"Categoria creada exitosamente"}, 201
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    #get id
    @classmethod
    def get_category(cls, id: int):
        """
        Get one category by id from DB
        
        Input: category's id

        Output:
        - CategoryModel with category's information, 200, if operation is successfull
        - If id is not found return 404
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM categories WHERE id={str(id)}')
                result = cursor.fetchone()
                if result:
                    category = Category(
                        result['id'],
                        result['title'],
                        result['type'],
                        )
                    return category, 200
                else:
                    return {'error':'Categoria no encontrada'}, 404
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    #put id
    @classmethod
    def update_category(cls, id: int, category: Category):
        """
        Update category by id in DB
        
        Input: 
        - id: int category's id
        - CategoryModel with updated information 
            - category.title -> str
            - category.type ENUM

        Output:
        - dictionary with message successfull and 201 if operation is successfull
        - if account is not found return dictionary with error mensage and HTTP 404
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            if not cls.category_exists(id):
                return {"error": "La categoria no fue encontrada."}, 404
            
            with connection.cursor() as cursor:
                cursor.execute(
                    'UPDATE categories SET title = "%s", type = "%s" WHERE id = %s' % 
                    (category.title, category.type, str(id)))
            connection.commit()
            return {'message':'Categoria actualizada exitosamente'}, 200
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    #delete id
    @classmethod
    def delete_category(cls, id: int):
        """
        Delete category by id in DB
        
        Input: category's id

        Output:
        - dictionary with message successfull and 200 if operation is successfull
        - if account is not found return dictionary with error mensage and HTTP 404
        - if exist error return dictionary with error mensage and HTTP 500
        """
        try:
            if not cls.category_exists(id):
                return {"error": "La categoria no fue encontrada."}, 404
            
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM categories WHERE id = %s' % (str(id)))
            connection.commit()
            return {'message':'Categoria eliminada exitosamente'}, 200
        except Exception as e:
            logging.debug(e)
            return {"error": 'Server Error'}, 500
    



    @classmethod
    def category_exists(cls, id: int):
        '''
        Verify if category exist

        Input: id
        
        Output:
        - True if exist
        - False if not exist or if exception occurs
        
        '''
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT id FROM categories WHERE id = %s' % (str(id)))
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            logging.debug(e)
            return False