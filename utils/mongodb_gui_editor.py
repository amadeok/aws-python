
from bson import ObjectId
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
os.chdir(parent_dir)
print("Working directory", os.getcwd())

import mongo_utils
import cloud_utils.mongo_schema as mongo_schema
import cloud_utils.mongo_client as mongo_client
from dotenv import load_dotenv
import tkinter as tk
from tkinter import scrolledtext
import json, copy
import settingsManager

from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # or str(obj) or any custom format
        return super().default(obj)

def find_first_from_right(target_string, string_list):
    max_index = -1
    result = None

    for s in string_list:
        if s in target_string:
            index = target_string.rfind(s)  # Find the last occurrence of s
            if index > max_index:
                max_index = index
                result = s

    return result

def list_to_nested_dict(keys, value):
    nested_dict = value
    for key in reversed(keys):
        nested_dict = {key: nested_dict}
    return nested_dict

def list_to_flat_dict(keys, value):
    return {".".join(keys): value}
class JsonEditorApp:
    def __init__(self, root):
        self.root = root
        bg_color = "#3b3b3b"
        root.configure(bg=bg_color)
        root.option_add("*background", "#444444")
        root.option_add("*foreground", "#ffffff")

        client = mongo_client.MongoDBClient(uri, 'social-media-helper',
                            {'track_entries': mongo_schema.trackSchema.schema, 
                            "upload_attempts": mongo_schema.uploadAttempt.schema,
                            "upload_sessions": mongo_schema.uploadSession.schema, 
                            "settings": None} )
    
        client2 = mongo_client.MongoDBClient(uri, 'cristiank_website',
                                {'newsletter_subscriber_emails': None, 
                                "user_emails": None,
                                "website_settings": None}, client=client.client )

        self.mongo_clients = {            
            "social-media-helper": { "client": client,
                                    "database" : mongo_utils.get_track_entries_(client), },
            "cristiank_website": { "client": client2,
                                    "database":mongo_utils.get_cristiank_website_entries(client2) }
            }

        self.fetch_databases()
        self.selected_database_name = "social-media-helper"
        self.data = self.get_database()
        self.starting_string = ""
        self.starting_projection_string = ""

        self.settings_manager = settingsManager.SettingsManager("querier_settings.json", defaults={"starting_string":"", "starting_projection_string":""}, target=self)
        self.settings_manager.load_settings()

        def save_func():
            self.starting_string = self.entry.get("1.0", tk.END).strip()
            self.starting_projection_string = self.projection_entry.get("1.0", tk.END).strip()
            self.settings_manager.save_settings()

        self.root.bind("<Control-s>", lambda e: save_func())

        self.setup_ui()
        self.set_entry_value(self.entry, self.starting_string)
        self.set_entry_value(self.projection_entry, self.starting_projection_string)

    def get_database(self):
        return self.mongo_clients[self.selected_database_name]["database"]
    def get_client(self):
        return self.mongo_clients[self.selected_database_name]["client"]
    
    def fetch_databases(self):
        print("fetching databases")
        self.mongo_clients["social-media-helper"]["database"] = mongo_utils.get_track_entries_(self.mongo_clients["social-media-helper"]["client"])
        self.mongo_clients["cristiank_website"]["database"] =  mongo_utils.get_cristiank_website_entries(self.mongo_clients["cristiank_website"]["client"])


    
    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:  
            self.fetch_databases()
            self.selected_database_name = self.listbox.get(selected_index)  
            self.data = self.get_database()
            print("using database:  ", self.selected_database_name)

    def set_entry_value(self, entry_, text):
        entry_.delete("1.0", tk.END)
        entry_.insert("1.0", text)

    def setup_ui(self):
        self.entry_label = tk.Label(self.root, text="Enter key or index path:")
        self.entry_label.pack(padx=10, pady=5)

        self.text_frame2 = tk.Frame(self.root)
        self.text_frame2.pack(side=tk.TOP, padx=10, pady=5, anchor="w")

        self.text_frame = tk.Frame(self.text_frame2)
        self.text_frame.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")

        # First text widget
        self.entry = tk.Text(self.text_frame, width=100, height=2, undo=True)
        self.entry.pack( padx=10, pady=5)
        self.entry.bind("<Return>", self.navigate_json)
        self.entry.bind("<Shift-Return>", lambda *args: self.update_json())

        # Second text widget
        self.projection_entry = tk.Text(self.text_frame, width=100, height=2, undo=True)
        self.projection_entry.pack(padx=10, pady=5)
        self.projection_entry.bind("<Return>", self.navigate_json)
        self.projection_entry.bind("<Shift-Return>", lambda *args: self.update_json())

        # Listbox aligned to the right of text widgets
        self.listbox = tk.Listbox(self.text_frame2, height=5)
        for key in self.mongo_clients.keys():
            self.listbox.insert(tk.END, key)
        self.listbox.pack(side=tk.RIGHT, padx=10, pady=5, anchor="w")


        self.listbox.bind("<<ListboxSelect>>", self.on_select)


        self.scroll_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier", 12), undo=True)
        self.scroll_text.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)

        self.update_button = tk.Button(self.root, text="Update JSON", command=self.update_json)
        self.update_button.pack(pady=10)
        self.scroll_text.bind("<Shift-Return>", lambda *args: self.update_json())

        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.pack(pady=5)

    def navigate_json(self, event=None):
        try:
            """Navigate through JSON using the given path."""
            user_input = self.entry.get("1.0", tk.END).strip()
            projection_input = self.projection_entry.get("1.0", tk.END).strip()
            if projection_input.__len__() > 1:
                if projection_input[0] == "+": 
                    projection_input = projection_input[1:]
                    default_include=True
                elif projection_input[0] == "-":
                    default_include=False
                    projection_input = projection_input[1:]
                else:default_include = True

            projection_data = json.loads(projection_input) if projection_input != "" else {}
            
            selected_data, prev_obj, _id = self.get_json_part(self.data, user_input)
            
            if projection_data != {}:
                
                if default_include:
                    final_data = copy.deepcopy(selected_data )
                    for k,v in projection_data.items():
                        if v == 0:
                            if type(selected_data) == dict:
                                del final_data[k]
                            else:
                                for i, elem in enumerate(selected_data):
                                    del final_data[i][k]
                            
                else:
                    final_data = {} if type(selected_data) == dict else [{} for e in selected_data]
                    for k,v in projection_data.items():
                        if v == 1:
                            if type(selected_data) == dict:
                                final_data.update({k:selected_data[k]})
                            else:
                                for i, elem in enumerate(selected_data):
                                    final_data[i].update({k:elem[k]})
            else:
                final_data = selected_data

            # print('final_data: ', final_data)


            json_string = json.dumps(final_data, indent=4,  cls=DateTimeEncoder)
            self.scroll_text.config(state=tk.NORMAL)
            self.scroll_text.delete(1.0, tk.END)
            self.scroll_text.insert(tk.END, json_string)
        except Exception as e:
            print("-->", e)
        finally:
            return "break"
#website_settings[{"_id":"67b94505da721aa2844cd02b"}]
    def get_json_part(self, json_obj, path):
        """Navigate JSON object based on a key/index/query path."""
        try:
            _id = None
            path_parts = self.parse_path(path)
            key = []
            for part in path_parts:
                if isinstance(json_obj, list):
                    if part.startswith("{") and part.endswith("}"):
                        query = json.loads(part)
                        key = []
                        json_obj = self.find_in_list(json_obj, query)
                    else:
                        key.append(int(part))
                        json_obj = json_obj[int(part)]
                else:
                    key.append(part)
                    json_obj = json_obj[part]
                if type(json_obj) == dict and "_id" in json_obj:
                    _id = json_obj["_id"]
            # if not len(key):
            #     key = [path_parts[0]]
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
        path = self.entry.get("1.0", tk.END).strip()
        try:
            edited_json = self.scroll_text.get(1.0, tk.END).strip()
            updated_data = json.loads(edited_json)

            self.set_json_part(self.data, path, updated_data)
            

            client :mongo_client.MongoDBClient= self.get_client()
            target_string = path
            string_list = client.collection_names

            result = find_first_from_right(target_string, string_list)
            print("collection determined:", result)  # Output: "hello"
            if result:

                selected_data, key,  _id = self.get_json_part(self.data, path)
                if not len(key):
                    update_data_ = updated_data
                else:
                    update_data_ = list_to_flat_dict(key, updated_data)
                # ori_database = self.get_database()
                # ori_database.update(update_data_)
                query = {"_id": ObjectId(_id)}

                ret = client.update_entry(query, update_data_, result, None, False, overwrite_doc= not len(key) )
                if not ret: raise Exception("Error updating database")
                print("mongo update res", ret, query)

            self.status_label.config(text="JSON updated successfully!", fg="#00ff00")
        except json.JSONDecodeError:
            self.status_label.config(text="Invalid JSON format!", fg="red")
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.status_label.config(text=f"Error: {str(e)}", fg="red")
        finally: 
            return 'break'

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




if __name__ == "__main__":
    
    argm = settingsManager.ArgParser(("env_file", str, ".env"))
    load_dotenv(argm.args.env_file)

    uri = os.getenv("MONGODB_URI")
    # script_dir = os.path.dirname(os.path.abspath(__file__))


    root = tk.Tk()
    root.title("JSON Editor")
    app = JsonEditorApp(root)
    root.mainloop()

