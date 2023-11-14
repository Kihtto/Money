import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

connection = pymysql.connect(host='localhost',
                             user=os.getenv('user'),
                             password=os.getenv('password'),
                             database='expense_management',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

### probar base de datos
# with connection.cursor() as cursor:
#    cursor.execute(f'SELECT * FROM accounts')
#    result = cursor.fetchall()
#print(result) 
# 
# ###