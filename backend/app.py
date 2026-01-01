from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes import main_routes
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    
    CORS(app)
    JWTManager(app)
    
    app.register_blueprint(main_routes)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
