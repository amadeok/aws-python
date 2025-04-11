// Sample data - list of dictionaries
let items = [
    {
        id: 1,
        name: "Product A",
        price: "19.99",
        category: "Electronics",
        inStock: true
    },
    {
        id: 2,
        name: "Product B",
        price: "29.99",
        category: "Home & Kitchen",
        inStock: false,
        rating: "4.5"
    },
    {
        id: 3,
        name: "Product C",
        price: "9.99",
        category: "Books",
        author: "John Doe"
    }
];

// Callback function when Enter is pressed
function onCellEdit(rowIndex, key, oldValue, newValue) {
    const statusElement = document.getElementById('status-message');
    
    // Validate the new value if needed
    if (key === 'price' && isNaN(parseFloat(newValue))) {
        statusElement.textContent = `Error: Price must be a number`;
        statusElement.className = 'status-message error';
        setTimeout(() => statusElement.className = 'status-message', 3000);
        return false; // Reject the change
    }
    
    // Update the data model
    items[rowIndex][key] = newValue;
    
    // Show success message
    statusElement.textContent = `Updated ${key} from "${oldValue}" to "${newValue}" in row ${rowIndex + 1}`;
    statusElement.className = 'status-message success';
    setTimeout(() => statusElement.className = 'status-message', 3000);
    
    // Here you could also send data to server
     saveToServer(items[rowIndex]);
    
    return true; // Accept the change
}

// Function to get all unique keys from the items
function getAllKeys(items) {
    const keys = new Set();
    items.forEach(item => {
        Object.keys(item).forEach(key => keys.add(key));
    });
    return Array.from(keys);
}

// Function to create editable cell
function createEditableCell(value, rowIndex, key) {
    const td = document.createElement('td');
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'editable-cell';
    input.value = formatValueForEditing(value);
    
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const oldValue = items[rowIndex][key];
            const newValue = parseEditedValue(key, input.value);
            
            if (onCellEdit(rowIndex, key, oldValue, newValue)) {
                input.value = formatValueForDisplay(newValue);
                input.blur();
            } else {
                input.value = formatValueForDisplay(oldValue);
            }
        } else if (e.key === 'Escape') {
            input.value = formatValueForDisplay(items[rowIndex][key]);
            input.blur();
        }
    });
    
    input.addEventListener('blur', () => {
        input.value = formatValueForDisplay(items[rowIndex][key]);
    });
    
    input.addEventListener('focus', () => {
        input.value = formatValueForEditing(items[rowIndex][key]);
    });
    
    td.appendChild(input);
    return td;
}

// Format value for display in the cell
function formatValueForDisplay(value) {
    if (value === undefined || value === null) return '';
    if (typeof value === 'boolean') return value ? '✓' : '✗';
    if (Array.isArray(value)) return value.join(', ');
    return value;
}

// Format value for editing in the input
function formatValueForEditing(value) {
    if (value === undefined || value === null) return '';
    if (typeof value === 'boolean') return value ? 'true' : 'false';
    if (Array.isArray(value)) return value.join(', ');
    return value;
}

// Parse edited value back to correct type
function parseEditedValue(key, value) {
    // You can add special parsing for certain fields
    if (key === 'inStock') {
        return value.toLowerCase() === 'true' || value === '1' || value.toLowerCase() === 'yes';
    }
    if (key === 'price' || key === 'rating') {
        return isNaN(parseFloat(value)) ? value : parseFloat(value).toString();
    }
    return value;
}

// Function to render the grid
function renderGrid(items) {
    const table = document.getElementById('data-grid');
    table.innerHTML = ''; // Clear existing content
    
    const allKeys = getAllKeys(items);
    
    // Create table header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    allKeys.forEach(key => {
        const th = document.createElement('th');
        th.textContent = key;
        headerRow.appendChild(th);
    });
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Create table body
    const tbody = document.createElement('tbody');
    
    items.forEach((item, rowIndex) => {
        const row = document.createElement('tr');
        
        allKeys.forEach(key => {
            const cellValue = item[key];
            
            if (key === 'id') {
                // Make ID non-editable
                const td = document.createElement('td');
                td.textContent = cellValue || '';
                row.appendChild(td);
            } else {
                // Create editable cell for other fields
                const td = createEditableCell(cellValue, rowIndex, key);
                row.appendChild(td);
            }
        });
        
        tbody.appendChild(row);
    });
    
    table.appendChild(tbody);
}

// Initial render
renderGrid(items);

// Example function to save to server
function saveToServer(item) {
    console.log('Saving to server:', item);
    // In a real app, you would use fetch() here
    fetch('/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({message: item})
    })
    .then(response => response.json())
    .then(data => console.log('Response:', data))
    .catch(error => console.error('Error:', error));

}