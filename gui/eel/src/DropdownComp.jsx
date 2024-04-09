import React, { useRef, useState } from 'react';
import { compRef } from './App';

const DropdownComponent = ({label, placeholder, options, selectedOption, handleSelectChange}) => {
  // State to manage the selected option
//   const [selectedOption, setSelectedOption] = useState('');

  // Function to handle changes in the dropdown selection
//   const handleSelectChange = (event) => {
//     setSelectedOption(event.target.value);
//     console.log("--------------- >  selectedOption", selectedOption)
//     // if (localStorage)
//     // localStorage.setItem("showing", page)
//   };
    // const selectRef = useRef()
  return (
    <div className='flex _h-[200px]  items-center'>
      <h2 className='h-fit'>{label}:</h2>
      <select value={selectedOption} onChange={handleSelectChange} className='  text-black rounded-md mx-3 h-fit'>
        <option value="">{placeholder}</option>
        {options&& options.map((option, i) => <option key={i} value={option._id}>{option.label}</option>)}
        
        {/* <option value="option2">Option 2</option>
        <option value="option3">Option 3</option> */}
      </select>
      {/* <p>Selected option: {compRef && compRef.state.track_entries && compRef.state.track_entries.find(item => item._id === selectedOption).track_title }</p> */}
    </div>
  );
};

export default DropdownComponent;
