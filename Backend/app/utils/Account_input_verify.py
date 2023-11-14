from markupsafe import escape
from flask import jsonify

def verify(title, initial_balance):
    title = escape(title)
    initial_balance = escape(initial_balance)
    
    if not title or not initial_balance:
        return jsonify({'error':'Datos incompletos'}), 400 
    
    try:
        initial_balance = int(initial_balance)
    except ValueError:
        return jsonify({'error':'Initial_balance debe ser un entero'}), 400
    
    return title, initial_balance