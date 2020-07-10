# import sqlite3
from flask_restful import (
    Resource,
    reqparse
)

from flask_jwt import (
    jwt_required
)

from models.item import ItemModel

# Create resource, actually they are endpoints


class Item(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="The cannot be left blank!"
    )
    parser.add_argument(
        'store_id',
        type=float,
        required=True,
        help="Every item need store!"
    )

    def post(self, name):
        if ItemModel.find_by_name(name):
            return (
                {'message': f"An item named '{name}' already exists."}, 400
            )
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured'}, 500
        return item.json(), 201  # to inform application we have created item

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': f"Item '{name}' does not found."}, 404

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occerd.'}
        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete_from_db()
                return {'message': f"Item '{name}' deleted."}
            except:
                return {'message': 'An error occerd.'}
        return (
            {'message': f"Unable to find item named '{name}'."}, 400
        )


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # return
        # {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
