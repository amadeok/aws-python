from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample data - in a real app you'd use a database
data = [
    {'id': 1, 'name': 'Alice', 'age': 28, 'city': 'New York'},
    {'id': 2, 'name': 'Bob', 'age': 34, 'city': 'Chicago'},
    {'id': 3, 'name': 'Charlie', 'age': 22, 'city': 'Los Angeles'},
    {'id': 4, 'name': 'Diana', 'age': 29, 'city': 'Miami'}
]

@app.route('/')
def display_grid():
    headers = data[0].keys() if data else []
    return render_template('grid.html', headers=headers, data=data)

@app.route('/update', methods=['POST'])
def update_data():
    try:
        # Get the updated data from the request
        updated_item = request.json
        
        # Find and update the item in our data list
        for i, item in enumerate(data):
            if item['id'] == updated_item['id']:
                data[i] = updated_item
                return jsonify({'status': 'success', 'message': 'Data updated'})
        
        return jsonify({'status': 'error', 'message': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)