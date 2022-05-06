import pymongo
from bson import ObjectId


# https://github.com/vfxpipeline/Python-MongoDB-Example/blob/master/lib/databaseOperations.py


class Database:
    def __init__(self, collection) -> None:
        # CONNECT TO DATABASE
        connection = pymongo.MongoClient("localhost", 27017)
        
        # CREATE DATABASE
        database = connection['my_database']

        # CREATE COLLECTION
        self.collection = database[collection]

        print("Database connected")

    def insert_data(self, data):
        """
        Insert new data or document in collection
        :param data:
        :return:
        """
        document = self.collection.insert_one(data)
        return document.inserted_id

    def update_or_create(self, id, data):
        """
        This will create new document in collection
        IF same document ID exist then update the data
        :param document_id:
        :param data:
        :return:
        """
        # TO AVOID DUPLICATES - THIS WILL CREATE NEW DOCUMENT IF SAME ID NOT EXIST
        document = self.collection.update_one({'id': id}, {"$set": data}, upsert=True)
        return document.acknowledged


    def get_single_data(self, id):
        """
        get document data by document ID
        :param document_id:
        :return:
        """
        data = self.collection.find_one({'id': id})
        return data

    def get_single_data_by_username(self, username):
        data = self.collection.find_one({'username': username})
        return data


    def get_multiple_data(self):
        """
        get all document data
        :return:
        """
        data = self.collection.find()
        return list(data)


    def update_existing(self, id, data):
        """
        Update existing document data by document ID
        :param document_id:
        :param data:
        :return:
        """
        document = self.collection.update_one({'id': id}, {"$set": data})
        return document.acknowledged


    def remove_data(self, id):
        document = self.collection.delete_one({'id': id})
        return document.acknowledged