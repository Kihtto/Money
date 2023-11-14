from markupsafe import escape
from flask import jsonify
from datetime import datetime

def verify(title, date, amount, type, account_id, category_id):
        title = escape(title)
        date = escape(date)
        amount = escape(amount)
        type = escape(type)
        account_id = escape(account_id)
        category_id = escape(category_id)
        
        if not title or not date or not amount or not type or not account_id or not category_id:
            return jsonify({'error':'Datos incompletos'}), 400 
        
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return ({'error':'date debe tener formato datetime YYYY-mm-dd'})
        
        try:
            amount = int(amount)
        except ValueError:
            return jsonify({'error':'amount debe ser un entero'}), 400
        
        try:
            type = int(type)
        except ValueError:
            return jsonify({'error':'type debe ser un entero entre 1 y 3'}), 400
        
        try:
            account_id = int(account_id)
        except ValueError:
            return jsonify({'error':'account_id debe ser un entero'}), 400
        
        try:
            category_id = int(category_id)
        except ValueError:
            return jsonify({'error':'category_id debe ser un entero'}), 400
        
        return title, date, amount, type, account_id, category_id