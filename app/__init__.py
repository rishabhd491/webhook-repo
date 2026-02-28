from flask import Flask
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv

load_dotenv()

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    
    # Use environment variable for MongoDB URI
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/webhook_db")
    
    mongo.init_app(app)
    
    with app.app_context():
        # Import and register blueprints
        from app.webhook.routes import webhook_bp
        app.register_blueprint(webhook_bp)
        
        # Add index route
        from flask import render_template
        @app.route("/")
        def index():
            return render_template("index.html")

    return app
