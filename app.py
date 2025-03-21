from flask import Flask
from database import init_db,db
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
from controllers.user_controller import user_bp
from controllers.book_controller import book_bp
from controllers.author_controller import author_bp


app = Flask(__name__)
init_db(app)
with app.app_context():
    db.create_all()

SWAGGER_URL = "/swagger" 
API_URL = "/static/swagger.json"  

swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL,config={
        "app_name": "Book API",
        "validatorUrl": None,
        "swaggerHeaders": [{"name": "Authorization", "value": "Bearer YOUR_JWT_TOKEN"}]
})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


app.config["JWT_SECRET_KEY"] = "THIS_IS_MY_BOOK_STORE_JWT_AUTHENTICATION_KEY"
jwt = JWTManager(app)

app.register_blueprint(user_bp)
app.register_blueprint(book_bp)
app.register_blueprint(author_bp)

if __name__ == "__main__":
    app.run(debug=True)
