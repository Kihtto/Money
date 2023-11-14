from app.models.CategoryModel import Category

def Category_to_json(category: Category):
    json = {
        'id': category.id,
        'title': category.title,
        'type': category.type
    }
    return json