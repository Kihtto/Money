from flask import request, jsonify, Blueprint
from app.models.CategoryModel import Category
from app.services.CategoriesServices import CategoryServices
from app.utils.Category_to_json import Category_to_json
from app.utils.Category_input_verify import verify


categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET','POST', 'DELETE'])
def categories():
    if request.method == 'GET':
        categories_response = CategoryServices.get_all_categories()
        if categories_response[1]==200:
            categories = [Category_to_json(category) for category in categories_response[0]]
            categories_response = (categories, categories_response[1])
        return jsonify(categories_response[0]), categories_response[1]
    elif request.method == 'POST':
        title, type = verify(
            request.json.get('title'),
            request.json.get('type'),)
        new_category = Category(0, title, type)
        response = CategoryServices.create_category(new_category)
        return jsonify(response[0]), response[1]
    else:
        response = CategoryServices.delete_all_categories()
        return jsonify(response[0]), response[1]

@categories_bp.route('/categories/<int:id>', methods=['GET','PUT', 'DELETE'])
def categories_id(id):
    if request.method == 'GET':
        response = CategoryServices.get_category(id)
        if response[1] == 200:
            response = (Category_to_json(response[0]), response[1])
        return jsonify(response[0]), response[1]
    elif request.method == 'PUT':
        title, type = verify(
            request.json.get('title'),
            request.json.get('type'),)
        updated_category = Category(id, title, type)
        response = CategoryServices.update_category(id, updated_category)
        return jsonify(response[0]), response[1]
    else:
        response = CategoryServices.delete_category(id)
        return jsonify(response[0]), response[1]