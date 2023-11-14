from markupsafe import escape
from flask import jsonify

def verify(title, type):
    title = escape(title)
    type = escape(type)
    
    if not title or not type:
        return jsonify({'error':'Datos incompletos'}), 400 
    
    try:
        type = int(type)
    except ValueError:
        return jsonify({'error':'type debe ser un entero entre 1 y 3'}), 400
    
    return title, type