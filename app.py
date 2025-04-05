from flask import Flask, jsonify
from flask_restful import Api
from models.models import db
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import traceback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootroot@localhost:3306/bank_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['WTF_CSRF_ENABLED'] = False 

from routes.routes import register_routes
register_routes(api)

@app.errorhandler(Exception)
def handle_exception(e):
    response = {
        "error": "Internal Server Error",
        "message": str(e)
    }

    error_traceback = traceback.format_exc()

    print(error_traceback)

    return jsonify(response), 500  # Return HTTP 500 status code

if __name__ == "__main__":
    app.run(debug=True)
