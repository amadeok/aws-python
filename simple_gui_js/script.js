
import { config } from "./aux_.js"

let database = []

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
    database[rowIndex][key] = newValue;

    // Show success message
    statusElement.textContent = `Updated ${key} from "${oldValue}" to "${newValue}" in row ${rowIndex + 1}`;
    statusElement.className = 'status-message success';
    setTimeout(() => statusElement.className = 'status-message', 3000);

    // Here you could also send data to server
    saveToServer(database[rowIndex]);

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
    const cell = document.createElement('div');
    cell.className = 'grid-cell';
    cell.dataset.row = rowIndex;
    cell.dataset.col = key;


    const conf = config[key]
    if (conf) {
        if ("parseFunc" in conf)
            value = conf["parseFunc"](value, cell)
        cell.style.gridColumn = `span ${"colWeight" in conf ? conf["colWeight"] : 1}`
    }

    const displaySpan = document.createElement('span');
    displaySpan.className = 'cell-display';
    displaySpan.textContent = formatValueForDisplay(value);

    const input = document.createElement('input');
    input.type = key == "insertion_date" ? "datetime-local" : 'text';
    input.className = 'cell-edit';
    input.value = formatValueForEditing(value);
    input.style.display = 'none';


    cell.appendChild(displaySpan);
    cell.appendChild(input);

    cell.addEventListener('click', () => {
        displaySpan.style.display = 'none';
        input.style.display = 'inline-block';
        input.focus();
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {

            const oldValue = database[rowIndex][key];

            const newValue = parseEditedValue(key, input.value, cell);

            if (onCellEdit(rowIndex, key, oldValue, newValue)) {
                displaySpan.textContent = formatValueForDisplay(newValue);
                displaySpan.style.display = 'inline-block';
                input.style.display = 'none';
            } else {
                input.value = formatValueForDisplay(oldValue);
            }
        } else if (e.key === 'Escape') {
            displaySpan.style.display = 'inline-block';
            input.style.display = 'none';
        }
    });

    input.addEventListener('blur', () => {
        displaySpan.style.display = 'inline-block';
        input.style.display = 'none';
    });

    return cell;
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
function parseEditedValue(key, value, cell) {

    const conf = config[key]
    if (conf && "parseFunc" in conf) {
        return conf["parseFunc"](value, cell)
    }
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
    const gridContainer = document.getElementById('data-grid');
    gridContainer.innerHTML = ''; // Clear existing content

    const allKeys = getAllKeys(items);

    gridContainer.style.display = 'grid';

    let extraCols = 0

    // Create header cells
    allKeys.forEach(key => {
        const headerCell = document.createElement('div');
        headerCell.className = 'grid-header';
        headerCell.textContent = key;

        const conf = config[key]
        if (conf) {
            let val = "colWeight" in conf ? conf["colWeight"] : 1
            headerCell.style.gridColumn = `span ${val}`
            extraCols += val - 1
        }

        gridContainer.appendChild(headerCell);
    });

    gridContainer.style.gridTemplateColumns = `repeat(${allKeys.length + extraCols}, 1fr)`;


    // Create data cells
    items.forEach((item, rowIndex) => {
        allKeys.forEach(key => {
            const cellValue = item[key];

            if (key === 'id') {
                // Make ID non-editable
                const cell = document.createElement('div');
                cell.className = 'grid-cell';
                cell.textContent = cellValue || '';
                gridContainer.appendChild(cell);
            } else {
                // Create editable cell for other fields
                const cell = createEditableCell(cellValue, rowIndex, key);
                gridContainer.appendChild(cell);
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', async function () {
    let response = await fetch('/get-database', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    let obj = await response.json()
    console.log("response", obj, obj.data.track_entries)
    // .then(response => response.json())
    // .then(data => console.log('Response:', data))
    // .catch(error => console.error('Error:', error));
    database = obj.data.track_entries
    renderGrid(database);

    console.log('DOM fully loaded and parsed');
});
// Initial render


// Example function to save to server
function saveToServer(item) {
    console.log('Saving to server:', item);

    fetch('/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: item })
    })
        .then(response => response.json())
        .then(data => console.log('Response:', data))
        .catch(error => console.error('Error:', error));
}