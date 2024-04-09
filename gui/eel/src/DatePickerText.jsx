import React, { useState, useRef, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import ClickOutsideDetector from './OutsideClickDetector';
import { formatDate } from './utils';

const DatePickerComponent = ({ label, value, style, path }) => {
  let date = new Date(value)
  const [selectedDate, setSelectedDate] = useState(date != "Invalid Date" ? date : new Date()); // Initial starting value
  const [isOpen, setIsOpen] = useState(false);
  // console.log("------->", date, selectedDate, date == "Invalid Date")
  const pickerRef = useRef(null)
  const clickCount = useRef(0)

  useEffect(() => {
    let date = new Date(value)
    setSelectedDate(date != "Invalid Date" ? date : new Date())
    return () => { }
  }, [value])

  useEffect(() => {
    return () => {   document.removeEventListener('mousedown', handleClickOutside);   }
  }, [])
  




  //console.log(date.toISOString());

  const handleChange = (e) => {
    clickCount.current += 1
    if (clickCount.current > 1) {
      setIsOpen(!isOpen);
      clickCount.current = 0
      eel.update_field({...path, value: e})
    }
    setSelectedDate(e);
  };

  const handleClickOutside = (event) => {
    console.log("handleClickOutside")
    if (pickerRef.current && !pickerRef.current.contains(event.target)) {
      setIsOpen(false);  
      clickCount.current = 0
      document.removeEventListener('mousedown', handleClickOutside);  
    }
  };
  const handleClick = (e) => {
    setTimeout(() => {
      if (clickCount.current == 0)
      document.addEventListener('mousedown', handleClickOutside);  
    }, 200);
    

    e.preventDefault();
    setIsOpen(!isOpen);
  };
  const handleBlur = (e) => {
  //  setTimeout(() => {
        // if (clickCount.current == 0) {
      setIsOpen(false);  
      clickCount.current = 0
        // }
      //}
  //  },200);
  };


  return (
    <div>
        <div className={` flex ${false ? "flex-col" : ""}`}>
          <div className='grow-[0] pr-2 _w-[100px] '>    {label}    </div>
        <button
          className="" onClick={handleClick}>
          {formatDate(selectedDate)}
        </button>
      </div>

      <div
        className='max-w-[2000px] absolute flex'
      // className={`${isOpen ? "h-[20px] w-[200px] block" : "_hidden   "}`}
      // className='absolute' onBlur={handleBlur} tabIndex={0} 
      > 
      <div ref={pickerRef} >
      {/* <ClickOutsideDetector onOutsideClick={handleBlur}> */}
        {isOpen && (
          <DatePicker selected={selectedDate} onChange={handleChange}
            // className='z-[1]'
            showTimeSelect
            inline
            // onBlur={handleBlur} tabIndex={0}
          />
        )}
        {/* </ClickOutsideDetector> */}
        </div>
        {isOpen &&
         ( <button onClick={()=> {clickCount.current = 0; setIsOpen(false)}} className='z-[1] h-[50px] w-[20px] rounded-2xl  bg-red-600'></button>)}
      </div>
    </div>
  );
};

export default DatePickerComponent;
