
#pymongo==3.11.0
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
from bson.objectid import ObjectId
from jsonschema import validate
from dotenv import load_dotenv
import os
import pyautogui
#import mongo_schema
load_dotenv()



class MongoDBClient:
    def __init__(self, connection_string, database_name, collection_schemas):
        self.client = MongoClient('localhost', 27017) if 0 else MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection_names = {key for key, value in collection_schemas.items() }
        self.collections = {key: self.db[key] for key, value in collection_schemas.items() }
        self.schemas = collection_schemas
        self.cd =  {name: [] for name in collection_schemas}
        
    def col(self, name): return self.collections[name]
    
    def fetch_entries(self, collection, query=None):
    
        if query is None:
            query = {}
        elems = list(self.col(collection).find(query))
        
        for entry in elems :  entry["_id"] = str(entry["_id"])

        return  elems

    # def create_entry(self, document):
    #     return collection.insert_one(document).inserted_id

    def delete_entry(self, query,collection ):
        return self.col(collection).delete_one(query)

    # def update_entry(self, query, update_data):
    #     return collection.update_one(query, {"$set": update_data})

    def update_entry(self, query, update_data, collection, schema=None):
        if not schema or  self.validate_document(update_data, schema):
            update_data_ = update_data.copy()
            del update_data_["_id"]
            return self.col(collection).update_one(query, {"$set": update_data_})
            print("Document updated successfully.")
        else:
            print("Document validation failed. Not inserted.")

    def create_entry(self, document, collection, schema=None):
        if not schema or  self.validate_document(document, schema):
            ret = self.col(collection).insert_one(document)
            document["_id"] = str(document["_id"])
            print("Document inserted successfully.")
            return ret
        else:
            print("Document validation failed. Not inserted.")

    def delete_all_in_collection(self, collection):
        result = pyautogui.confirm(f'Are you sure you want to delete all entries in collection {collection}?', buttons=['OK', 'Cancel'])

        # Check the user's choice
        if result == 'OK':
            result = self.col(collection).delete_many({})
            print(result.deleted_count, "documents deleted.")
            print('OK clicked')
        elif result == 'Cancel':
            print('Cancel clicked')
        


    def validate_document_for_upload(self, data, schema_  ):
        for elem in data:
            if not elem in schema_["properties"]:
                return False
        return True

    def validate_document(self, document, schema_  ):
        try:
            validate(instance=document, schema=schema_)
            return True
        except Exception as e:
            print("Validation Error:", e)
            return False


# Example usage:
if __name__ == "__main__":
    uri = os.getenv("MONGODB_URI")

    schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["name", "age", "email"]
}   
    # Initialize MongoDBClient with your connection string, database name, and collection name
    mongo_client = MongoDBClient(uri, 'social-media-helper',
                             {'track_entries': mongo_schema.trackSchema.schema, 
                              "upload_attempts": mongo_schema.uploadAttempt.schema,
                              "upload_sessions": mongo_schema.uploadSession.schema} )
    mongo_client.delete_all_in_collection("upload_attempts")
    exit()
    # Fetch entries
    entries = mongo_client.fetch_entries()
    print("Existing entries:", entries)

    example_document = {
        "name": "John Doe123",
        "age": 31232,
        "email": "john2@example.com",
        "test": "123"
    }

    #mongo_client.create_entry(example_document)

    new_entry = {"name": "Alice", "age": 25, "email": "alice@example.com"}
    new_entry_id = mongo_client.create_entry(new_entry)
    print("New entry ID:", new_entry_id)

    entries_after_insertion = mongo_client.fetch_entries()
    print("Entries after insertion:", entries_after_insertion)

    update_query = {"name": "Alice"}
    update_data = {"age": 26, "name": "rose"}
    update_result = mongo_client.update_entry(update_query, update_data, schema)
    if update_result:
        print("Update result:", update_result.modified_count)

    # Fetch entries after update
    entries_after_update = mongo_client.fetch_entries()
    print("Entries after update:", entries_after_update)

    # Delete entry
    delete_query = {"_id": ObjectId("65fc32319baf6eeae3d8e352")}
    delete_result = mongo_client.delete_entry(delete_query)
    print("Delete result:", delete_result.deleted_count)

    # Fetch entries after deletion
    entries_after_deletion = mongo_client.fetch_entries()
    print("Entries after deletion:", entries_after_deletion)
    
    # Close connection
    mongo_client.client.close()


# Create a new client and connect to the server
# client = MongoClient(uri)
# db = client['social-media-helper'] #database
# collection = db['track-task'] #collection

# document = {
#     "name": "John Doe2",
#     "age": 1,
#     "email": "john.daoe@example.com"
# }

# # Insert the document into the collection
# inserted_document_id = collection.insert_one(document).inserted_id

# print("Inserted document ID:", inserted_document_id)
# cursor = collection.find({})

# # Print the documents
# for document in cursor:
#     print(document)
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)