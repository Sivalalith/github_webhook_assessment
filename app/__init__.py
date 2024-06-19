from flask import Flask

from app.webhook.routes import webhook

from app.extensions import init_app


# Creating our flask app
def create_app():

    app = Flask(__name__, template_folder= '../templates')
    
    app.config['MONGO_URI'] = "mongodb+srv://<username>:<password>@cluster0.0ys2zcn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    app.config['MONGO_DBNAME'] = "MyDatabase"

    # Initialize MongoDB setup
    init_app(app)

    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app