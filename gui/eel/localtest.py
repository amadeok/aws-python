#from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://amadeokusch:iCnXlBqHY4nsijdg@cluster0.fno24h1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#uri = "mongodb://TEST:1deardeer@ac-06k6n6d-shard-00-00.k9qacs9.mongodb.net:27017,ac-06k6n6d-shard-00-01.k9qacs9.mongodb.net:27017,ac-06k6n6d-shard-00-02.k9qacs9.mongodb.net:27017/?ssl=true&replicaSet=atlas-9m1p34-shard-0&authSource=admin&retryWrites=true&w=majority"

#client = MongoClient("mongodb://amadeokusch:iCnXlBqHY4nsijdg@cluster0.fno24h1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Assuming MongoDB is running on the default port
# uri = "mongodb://amadeokusch:iCnXlBqHY4nsijdg@ac-ne4vxmj-shard-00-00.fno24h1.mongodb.net:27017,ac-ne4vxmj-shard-00-01.fno24h1.mongodb.net:27017,ac-ne4vxmj-shard-00-02.fno24h1.mongodb.net:27017/?ssl=true&replicaSet=atlas-nyxan3-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
client.admin.command('ping')

#MongoClientURI mongoUri  = new MongoClientURI("mongodb://Dbuser:dbpass@ds047692.mongolab.com:47692");

# Access a database
db = client['mydatabase']

# Access a collection
collection = db['mycollection']

# Insert a document
document = {"name": "John", "age": 30}
inserted_document = collection.insert_one(document)

# Find one document
result = collection.find_one({"name": "John"})
print(result)

# Close the connection
client.close()