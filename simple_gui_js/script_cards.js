// Sample data - list of dictionaries
const items = [
    {
        id: 1,
        name: "Product A",
        price: "$19.99",
        category: "Electronics",
        description: "High-quality gadget with advanced features"
    },
    {
        id: 2,
        name: "Product B",
        price: "$29.99",
        category: "Home & Kitchen",
        inStock: true,
        rating: 4.5
    },
    {
        id: 3,
        name: "Product C",
        price: "$9.99",
        category: "Books",
        author: "John Doe",
        pages: 250
    },
    {
        id: 4,
        name: "Product D",
        price: "$49.99",
        category: "Fashion",
        color: "Blue",
        sizes: ["S", "M", "L"]
    },
    {
        id: 5,
        name: "Product E",
        price: "$14.99",
        category: "Sports",
        weight: "1.2kg"
    }
];

// Function to create a card for each dictionary item
function createCard(item) {
    const card = document.createElement('div');
    card.className = 'card';
    
    // Create title from name or id if name doesn't exist
    const title = document.createElement('h3');
    title.textContent = item.name || `Item ${item.id}`;
    card.appendChild(title);
    
    // Add all other key-value pairs
    for (const [key, value] of Object.entries(item)) {
        // Skip id and name since we already used them
        if (key === 'id' || key === 'name') continue;
        
        const p = document.createElement('p');
        
        // Handle array values
        if (Array.isArray(value)) {
            p.innerHTML = `<span class="key">${key}:</span> ${value.join(', ')}`;
        } 
        // Handle boolean values
        else if (typeof value === 'boolean') {
            p.innerHTML = `<span class="key">${key}:</span> ${value ? 'Yes' : 'No'}`;
        }
        // Handle all other values
        else {
            p.innerHTML = `<span class="key">${key}:</span> ${value}`;
        }
        
        card.appendChild(p);
    }
    
    return card;
}

// Function to render all items in the grid
function renderGrid(items) {
    const gridContainer = document.getElementById('grid-container');
    gridContainer.innerHTML = ''; // Clear existing content
    
    items.forEach(item => {
        const card = createCard(item);
        gridContainer.appendChild(card);
    });
}

// Initial render
renderGrid(items);

// Optional: Function to filter or update the grid dynamically
function updateGrid(newItems) {
    renderGrid(newItems);
}

// Example of how to add a new item dynamically
document.addEventListener('DOMContentLoaded', () => {
    // You could add event listeners here for adding/removing items
    // For example:
    setTimeout(() => {
        const newItem = {
            id: 6,
            name: "New Product",
            price: "$39.99",
            category: "Toys",
            ageRange: "3-8 years"
        };
        items.push(newItem);
        updateGrid(items);
    }, 3000);
});