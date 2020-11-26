from pymongo import MongoClient


class MyMongo:

    def __init__(self, host, port):
        self._client = MongoClient(host, port)

    def __switch_database_collection(self, database, collection):
        """
        切换database和collection
        :param database:
        :param collection:
        :return:
        """
        self._database = self._client.get_database(database)
        self._collection = self._database.get_collection(collection)

    def search(self, database, collection, filter_condition):
        self.__switch_database_collection(database, collection)
        result = list(self._collection.find(filter_condition))
        for item in result:
            item['_id'] = str(item['_id'])
        return result

    def insert(self, database, collection, document):
        self.__switch_database_collection(database, collection)
        if isinstance(document, dict):
            result = self._collection.insert_one(document)
            return str(result.inserted_id)
        else:
            result = self._collection.insert_many(document)
            return list(result.inserted_ids)

    def update(self, database, collection, filter_condition, document):
        self.__switch_database_collection(database, collection)
        result = self._collection.update_one(filter_condition, {'$set': document})
        return result.modified_count

    def delete(self, database, collection, filter_condition):
        self.__switch_database_collection(database, collection)
        result = self._collection.delete_one(filter_condition)
        return result.deleted_count

    def aggregate(self, database, collection, pipeline):
        self.__switch_database_collection(database, collection)
        return list(self._collection.aggregate(pipeline))

    def __del__(self):
        self._client.close()


