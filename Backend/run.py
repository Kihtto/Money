from app import app
from app.routes.AccountsRoutes import accounts_bp
from app.routes.CategoriesRoutes import categories_bp
from app.routes.TransactionsRoutes import transactions_bp
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

app.register_blueprint(accounts_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(transactions_bp)

if __name__ == "__main__":
    app.run(debug=True)