# It's a user object
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="Cannot be blank!"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Cannot be blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"Message": f"User {data['username']} already exists."}, 400
        # user = UserModel(data['username'], data['password'])
        # unpacking:
        user = UserModel(**data)
        user.save_to_db()
        return (
            {"message": f"User '{data['username']}' created successfully."},
            201
        )

    def get(self):
        result = {}
        connection = sqlite3.connect('data.sql')
        cursor = connection.cursor()

        query = "SELECT * FROM users"

        for user in cursor.execute(query):
            result.add(user)

        connection.commit()
        connection.close()

        if result == {}:
            return {"message": "no users available"}
        return result


class UserList(Resource):
    def get(self):
        # return {'users': [user.json() for user in UserModel.query.all()]}
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}

