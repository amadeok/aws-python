
from bson import ObjectId
import eel_utils
import mongo_utils
import cloud_utils.mongo_schema as mongo_schema
import cloud_utils.mongo_client as mongo_client, os, sys
from dotenv import load_dotenv
load_dotenv()
import tkinter as tk
from tkinter import scrolledtext
import json
import settingsManager

def find_first_from_right(target_string, string_list):
    max_index = -1
    result = None

    # Iterate through the list
    for s in string_list:
        if s in target_string:
            # Find the index of the substring in the target string
            index = target_string.rfind(s)  # Find the last occurrence of s
            if index > max_index:
                max_index = index
                result = s

    return result



class JsonEditorApp:
    def __init__(self, root, data, mongo_instance=None):
        self.mongo : mongo_client.MongoDBClient = mongo_instance
        self.root :tk.Tk = root
        bg_color = "#3b3b3b"
        root.configure(bg=bg_color)
        root.option_add("*background", "#444444")
        root.option_add("*foreground", "#ffffff")

        self.data = data
        self.starting_string = ""

        self.settings_manager = settingsManager.SettingsManager("querier_settings.json", defaults={"starting_string":""}, target=self)
        self.settings_manager.load_settings()
        def save_func():
            self.starting_string =  self.entry.get().strip()
            self.settings_manager.save_settings()

        self.root.bind("<Control-s>", lambda e: save_func())


        self.setup_ui()
        self.set_entry_value(self.starting_string)


    def set_entry_value(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)

    def setup_ui(self):
        self.entry_label = tk.Label(self.root, text="Enter key or index path:")
        self.entry_label.pack(padx=10, pady=5)

        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(padx=10, pady=5)
        self.entry.bind("<Return>", self.navigate_json)

        self.scroll_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier", 12))
        self.scroll_text.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)

        self.update_button = tk.Button(self.root, text="Update JSON", command=self.update_json)
        self.update_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.pack(pady=5)

    def navigate_json(self, event=None):
        """Navigate through JSON using the given path."""
        user_input = self.entry.get().strip()
        selected_data, prev_obj, _id = self.get_json_part(self.data, user_input)
        
        json_string = json.dumps(selected_data, indent=4)
        self.scroll_text.config(state=tk.NORMAL)
        self.scroll_text.delete(1.0, tk.END)
        self.scroll_text.insert(tk.END, json_string)

    def get_json_part(self, json_obj, path):
        """Navigate JSON object based on a key/index/query path."""
        try:
            _id = None
            path_parts = self.parse_path(path)
            key = None
            for part in path_parts:
                if isinstance(json_obj, list):
                    if part.startswith("{") and part.endswith("}"):
                        query = json.loads(part)
                        key = query
                        json_obj = self.find_in_list(json_obj, query)
                    else:
                        key = int(part)
                        json_obj = json_obj[int(part)]
                else:
                    key = part
                    json_obj = json_obj[part]
                if type(json_obj) == dict and "_id" in json_obj:
                    _id = json_obj["_id"]

            return json_obj, key, _id
        except (KeyError, IndexError, ValueError) as e:
            return {"error": "Invalid path"}, None, None

    def find_in_list(self, json_list, query):
        """Find an object in a list based on a key-value query."""
        if not isinstance(json_list, list) or not isinstance(query, dict):
            raise ValueError("Invalid list or query format")

        for item in json_list:
            if isinstance(item, dict) and all(item.get(k) == v for k, v in query.items()):
                return item

        raise ValueError("No matching object found")

    def update_json(self):
        """Update a specific JSON field based on the input path."""
        path = self.entry.get().strip()
        try:
            edited_json = self.scroll_text.get(1.0, tk.END).strip()
            updated_data = json.loads(edited_json)

            self.set_json_part(self.data, path, updated_data)
            
            if self.mongo:
                target_string = path
                string_list = self.mongo.collection_names

                result = find_first_from_right(target_string, string_list)
                print(result)  # Output: "hello"
                if result:
                    selected_data, key,  _id = self.get_json_part(self.data, path)
                    query = {"_id": ObjectId(_id)}
                    update_data_  = {key: updated_data}
                    ret = self.mongo.update_entry(query, update_data_, result, self.mongo.schemas[result], True )
                    print("mongo update res", ret, query)

            self.status_label.config(text="JSON updated successfully!", fg="#00ff00")
        except json.JSONDecodeError:
            self.status_label.config(text="Invalid JSON format!", fg="red")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg="red")

    def set_json_part(self, json_obj, path, value):
        """Modify the correct part of the JSON object."""
        path_parts = self.parse_path(path)
        for part in path_parts[:-1]:
            if isinstance(json_obj, list):
                if part.startswith("{") and part.endswith("}"):
                    query = json.loads(part)
                    json_obj = self.find_in_list(json_obj, query)
                else:
                    json_obj = json_obj[int(part)]
            else:
                json_obj = json_obj[part]

        last_part = path_parts[-1]

        if isinstance(json_obj, list):
            if last_part.startswith("{") and last_part.endswith("}"):
                query = json.loads(last_part)
                for item in json_obj:
                    if isinstance(item, dict) and all(item.get(k) == v for k, v in query.items()):
                        item.update(value)  # Update found object
                        return
                raise ValueError("No matching object found to update")
            else:
                json_obj[int(last_part)] = value
        else:
            json_obj[last_part] = value

    def parse_path(self, path):
        """Parse JSON path into list of keys/indices/queries."""
        parts = []
        temp = ""
        i = 0
        while i < len(path):
            if path[i] == ".":
                if temp:
                    parts.append(temp)
                    temp = ""
            elif path[i] == "[":
                if temp:
                    parts.append(temp)
                    temp = ""
                i += 1
                start = i
                while i < len(path) and path[i] != "]":
                    i += 1
                parts.append(path[start:i])
            else:
                temp += path[i]
            i += 1
        if temp:
            parts.append(temp)
        return parts

# # Sample JSON Data
# data = {
#     "name": "John Doe",
#     "age": 30,
#     "email": "johndoe@example.com",
#     "is_active": True,
#     "address": {
#         "street": "123 Main St",
#         "city": "Anytown",
#         "state": "AN",
#         "zip": "12345"
#     },
#     "hobbies": ["reading", "coding", "hiking"],
#     "friends": [
#         {"name": "Jane", "age": 28},
#         {"name": "Mike", "age": 35}
#     ]
# }



if __name__ == "__main__":


    uri = os.getenv("MONGODB_URI")

    client = mongo_client.MongoDBClient(uri, 'social-media-helper',
                            {'track_entries': mongo_schema.trackSchema.schema, 
                            "upload_attempts": mongo_schema.uploadAttempt.schema,
                            "upload_sessions": mongo_schema.uploadSession.schema, 
                            "settings": None} )
    
    database = mongo_utils.get_track_entries_(client)
    # json_string = json.dumps(database, indent=4)


    root = tk.Tk()
    root.title("JSON Editor")
    app = JsonEditorApp(root, database, client)
    root.mainloop()


    # root = tk.Tk()
    # root.title("JSON Display with Scroll")

    # # Create a ScrolledText widget to display the JSON string
    # scroll_text = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD, font=("Courier", 12))
    # scroll_text.pack(padx=20, pady=20)

    # # Insert the JSON string into the ScrolledText widget
    # scroll_text.insert(tk.END, json_string)

    # # Disable editing the content
    # scroll_text.config(state=tk.DISABLED)

    # # Run the Tkinter event loop
    # root.mainloop()