import React, { useState } from 'react';

function DynamicWidthElements() {
  // Define state to hold element data, including width and style
  const [elements, setElements] = useState([
    { id: 1, width: '100px', backgroundColor: 'red' },
    { id: 2, width: '150px', backgroundColor: 'blue' },
    { id: 3, width: '200px', backgroundColor: 'green' }
  ]);

  // Function to handle changes in width
  const handleWidthChange = (id, newWidth) => {
    setElements(prevElements =>
      prevElements.map(element =>
        element.id === id ? { ...element, width: newWidth } : element
      )
    );
  };

  // Function to add a new element
  const addElement = () => {
    const newElement = {
      id: elements.length + 1,
      width: '100px',
      backgroundColor: 'yellow' // Example default background color for new elements
    };
    setElements(prevElements => [...prevElements, newElement]);
  };

  return (
    <div className=' '>
            <div className='flex '>

      {/* Render elements with dynamically set widths */}
        {elements.map(element => (
            <div
            key={element.id}
            style={{
                width: element.width,
                height: "50px",
                backgroundColor: element.backgroundColor
            }}
            >
            {/* Element {element.id}
            <input
                type="text"
                value={element.width}
                onChange={(e) => handleWidthChange(element.id, e.target.value)}
            /> */}
            </div>
        ))}

      {/* Button to add a new element */}
    </div>         <button onClick={addElement}>Add Element</button>
 </div>

  );
}

export default DynamicWidthElements;
