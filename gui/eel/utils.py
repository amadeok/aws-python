def get_field_current(obj, path):
    keys = path.split('.')
    current = obj

    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    last_key = keys[-1]
    return current[last_key]

def check_type(current):
    if not isinstance(current, list):
        raise ValueError('The specified path does not point to an array.')

def update_nested_field(obj, path, index, field, value):
    current = get_field_current(obj, path)

    if field is None:
        if index is None:
            current = value
        else:
            check_type(current)
            current[index] = value
    else:
        if index is None:
            current[field] = value
        else:
            check_type(current)
            current[index][field] = value

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
