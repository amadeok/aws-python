import React, { useState } from 'react';
import { eel } from "./eel.js";

function CheckboxComponent({value, label, style, path}) {
  const [isChecked, setIsChecked] = useState(value);

  const handleCheckboxChange = (event) => {
    setIsChecked(event.target.checked);
    console.log("event.target.checked", event.target.checked)
    if (path)
      eel.update_field({ ...path, value: event.target.checked })

  };

  return (
    <div className={`${style} flex`}>
      {/* <label> */}
        <div className='pr-2 w-fit'>
          {label}
        </div>

      {/* </label> */}
      <input
        type="checkbox"
        checked={isChecked}
        onChange={handleCheckboxChange}
      />
    </div>
  );
}

export default CheckboxComponent;
