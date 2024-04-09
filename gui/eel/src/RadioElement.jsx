import React from 'react';

function RadioComponent({ style, label, selectedOption, setSelectedOption, values }) {

    // const onOptionChange = (event) => {
    //     setSelectedOption(event.target.value);
    //   };

  return (

    <div className={`flex  items-center`}>
        <div className='px-2'>{label}</div>
        {values.map((value, i) => (
            module(value, i)
        ))}

    </div>
  );

    function module(value, i) {
        return <div key={i} className='px-[5px]'>
            <label>
                <input
                    type="radio"
                    value={value}
                    checked={selectedOption === value}
                    onChange={setSelectedOption} />
                {value}
            </label>
            {/* <br /> */}
        </div>;
    }
}

export default RadioComponent;
