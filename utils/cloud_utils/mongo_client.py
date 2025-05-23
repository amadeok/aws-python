
#pymongo==3.11.0
import logging
import time
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
from bson.objectid import ObjectId
from jsonschema import validate
from dotenv import load_dotenv
import os
import pyautogui
import certifi

load_dotenv()



class MongoDBClient:
    def __init__(self, connection_string, database_name, collection_schemas, client=None, local=False):
        ca = certifi.where()

        logging.info(f"initailizing monbodb client with string")
        if local:
            self.client = MongoClient('localhost', 27017, tlsCAFile=ca) 
        else:
            self.client = client if client else MongoClient(connection_string,  tlsCAFile=ca) #changing dns to 8.8.4.4 fixed it once
        
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

    def update_entry(self, query, update_data, collection, schema=None, soft_validate=False):
        if not schema or  self.validate_document(update_data, schema, soft_validate):
            update_data_ = update_data.copy()
            if "_id" in update_data_:
                del update_data_["_id"]
            return self.col(collection).update_one(query, {"$set": update_data_})
            logging.info("Document updated successfully.")
        else:
            logging.info("Document validation failed. Not inserted.")

    def create_entry(self, document, collection, schema=None):
        if not schema or  self.validate_document(document, schema):
            ret = self.col(collection).insert_one(document)
            document["_id"] = str(document["_id"])
            logging.info("Document inserted successfully.")
            return ret
        else:
            logging.info("Document validation failed. Not inserted.")

    def delete_all_in_collection(self, collection):
        result = pyautogui.confirm(f'Are you sure you want to delete all entries in collection {collection}?', buttons=['OK', 'Cancel'])

        # Check the user's choice
        if result == 'OK':
            result = self.col(collection).delete_many({})
            logging.info(f"{result.deleted_count} documents deleted.")
            logging.info('OK clicked')
        elif result == 'Cancel':
            logging.info('Cancel clicked')
        


    def validate_document_for_upload(self, data, schema_  ):
        for elem in data:
            if not elem in schema_["properties"]:
                return False
        return True

    def validate_document(self, document: dict, schema_, soft_validate=False  ):
        if not soft_validate:
            try:
                validate(instance=document, schema=schema_)
                return True
            except Exception as e:
                logging.error(f"Validation Error: {e}")
                return False
        else:
            all_keys_present = document.keys() <= schema_["properties"].keys()
            return all_keys_present
            # if not all_keys_present: return False
            # for k, val in document.items():
            #     if not schema_["properties"][k] == 



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
    time.sleep(20)
    #mongo_client.delete_all_in_collection("upload_attempts")
    exit()
    # Fetch entries
    entries = mongo_client.fetch_entries()
    logging.info("Existing entries:", entries)

    example_document = {
        "name": "John Doe123",
        "age": 31232,
        "email": "john2@example.com",
        "test": "123"
    }

    #mongo_client.create_entry(example_document)

    new_entry = {"name": "Alice", "age": 25, "email": "alice@example.com"}
    new_entry_id = mongo_client.create_entry(new_entry)
    logging.info("New entry ID:", new_entry_id)

    entries_after_insertion = mongo_client.fetch_entries()
    logging.info("Entries after insertion:", entries_after_insertion)

    update_query = {"name": "Alice"}
    update_data = {"age": 26, "name": "rose"}
    update_result = mongo_client.update_entry(update_query, update_data, schema)
    if update_result:
        logging.info("Update result:", update_result.modified_count)

    # Fetch entries after update
    entries_after_update = mongo_client.fetch_entries()
    logging.info("Entries after update:", entries_after_update)

    # Delete entry
    delete_query = {"_id": ObjectId("65fc32319baf6eeae3d8e352")}
    delete_result = mongo_client.delete_entry(delete_query)
    logging.info("Delete result:", delete_result.deleted_count)

    # Fetch entries after deletion
    entries_after_deletion = mongo_client.fetch_entries()
    logging.info("Entries after deletion:", entries_after_deletion)
    
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

# logging.info("Inserted document ID:", inserted_document_id)
# cursor = collection.find({})

# # logging.info the documents
# for document in cursor:
#     logging.info(document)
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     logging.info("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     logging.info(e)