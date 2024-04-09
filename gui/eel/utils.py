def get_field_current(obj, path):
    keys = path.split('.')
    current = obj

    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    last_key = keys[-1]
    return current, last_key

def check_type(current):
    if not isinstance(current, list):
        raise ValueError('The specified path does not point to an array.')

def update_nested_field(obj, path, index, field, value):
    current, last_key = get_field_current(obj, path)

    if field is None:
        if index is None:
            current[last_key] = value
        else:
            check_type(current[last_key])
            current[last_key][index] = value
    else:
        if index is None:
            current[last_key][field] = value
        else:
            check_type(current)
            current[last_key][index][field] = value

def add_to_field(obj, path, field, value):
    current = get_field_current(obj, path)
    check_type(current)

    if field is None:
        current.append(value)
    else:
        current[field].append( value)
    
def delete_field(obj, path, field, index):
    current = get_field_current(obj, path)
    check_type(current)

    if field is None:
        del current[index]
    else:
        del current[field][index]

    
def find_element_by_id(array, target_id):
    return next((element for element in array if element.get('_id') == target_id), None)


def merge_arrays(arr1, arr2, arr1_field_name, arr2_field_name):
    # Create a dictionary with _id as keys and corresponding objects from arr2 as values
    id_dict = {}
    for obj in arr2:
        _id = obj[arr2_field_name] #'track_entry_id'
        if _id not in id_dict:
            id_dict[_id] = []
        id_dict[_id].append(obj)

    # Merge arr1 and arr2
    for obj in arr1:
        _id = obj[arr2_field_name]
        if _id in id_dict:
            obj[arr1_field_name] = id_dict[_id]
        else:
            obj[arr1_field_name] = []

    return arr1

# obj = {
#     'a': {
#         'b': {
#             'c': [
#                 {'id': 1, 'name': 'Alice'},
#                 {'id': 2, 'name': 'Bob'},
#                 {'id': 3, 'name': 'Charlie'}
#             ],
#             'd': [
#                 "car", "shift", "boat"
#             ]
#         },
#         'e': "crack"
#     }
# }

# update_nested_field(obj, 'a.b.c', 1, 'name', 'Updated Bob')
# update_nested_field(obj, 'a.b.d', 2, None, 'Updated boat')
# update_nested_field(obj, 'a.e', None, None, 'Updated crack')

# print(obj)
