import os

from flask import Flask
from flask_restful import Api

from flask_jwt import JWT

# from db import db
from security import authenticate, identity
from resources.user import UserRegister, UserList
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)

# Flask application configurations:
app.config['DEBUG'] = True
# Place where to keep SQLite data:
app.config['SQLALCHEMY_DATABASE_URI'] = \
    os.environ.get('DATABASE_URL', 'sqlite:///data.sql')
# Keep SQLAlcheny responsiblt in tracking changes:
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.secret_key = 'Sergey'
api = Api(app)

# /auth end point
jwt = JWT(app, authenticate, identity)


# Test root message
@app.route('/')
def home():
    return "<h1 style='color:red'>Home page!</h1>"


# Add resources to the application
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserList, '/users')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
