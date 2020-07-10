from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f"A store '{name}' already exitsts."}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': f"Saving store '{name}' was unsuccessful"}, 500
        return store.json(), 201

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': f"Store '{name}' has not been found"}, 404

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': f"A store '{name}' has been deleted."}, 200
        return {'message': f"We are inable to find store'{name}'"}


class StoreList(Resource):
    def get(self):
        return {
            'stores': list(map(lambda x: x.json(), StoreModel.query.all()))
        }
