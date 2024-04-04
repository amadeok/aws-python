import React from 'react';

function RadioComponent({ style, label, selectedOption, setSelectedOption, values }) {

    const onOptionChange = (event) => {
        setSelectedOption(event.target.value);
      };

  return (

    <div className={`${style}`}>
        <div className='px-2'>{label}</div>
        {values.map((value) => (
            module(value)
        ))}

    </div>
  );

    function module(value) {
        return <div className='px-[5px]'>
            <label>
                <input
                    type="radio"
                    value={value}
                    checked={selectedOption === value}
                    onChange={onOptionChange} />
                {value}
            </label>
            {/* <br /> */}
        </div>;
    }
}

export default RadioComponent;
