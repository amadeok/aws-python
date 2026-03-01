import utils.cloud_utils.mongo_client as mongo_client, mongo_schema, os, sys
from dotenv import load_dotenv
load_dotenv()



# Example usage:
if __name__ == "__main__":

    if len(sys.argv)> 1:
        print(sys.argv)
        uri = os.getenv("MONGODB_URI")

        mongo_client = mongo_client.MongoDBClient(uri, 'social-media-helper',
                             {'track_entries': mongo_schema.trackSchema.schema, 
                              "upload_attempts": mongo_schema.uploadAttempt.schema,
                              "upload_sessions": mongo_schema.uploadSession.schema} )
        mongo_client.delete_all_in_collection(sys.argv[1])
    else:
        print("delete choises are track_entries upload_attempts upload_sessions")
    