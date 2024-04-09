import React, { useState, useRef, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const DatePickerComponent2 = ({ label, value, style, path }) =>  {
  const [startDate, setStartDate] = useState(new Date());
  const [isOpen, setIsOpen] = useState(false);
  const handleChange = (e) => {
    setIsOpen(!isOpen);
    setStartDate(e);
  };
  const handleClick = (e) => {
    e.preventDefault();
    setIsOpen(!isOpen);
  };
  return (
    <>
      <button className="example-custom-input" onClick={handleClick}>
        {startDate.toISOString()}
      </button>
      {isOpen && (
        <DatePicker selected={startDate} onChange={handleChange} inline />
      )}
    </>
  );
};
export default DatePickerComponent2;
